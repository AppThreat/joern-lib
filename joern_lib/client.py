import asyncio
import os

import httpx
import orjson
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import websockets

from joern_lib.utils import (
    check_labels_list,
    expand_search_str,
    print_flows,
    print_md,
    print_table,
)

headers = {"Content-Type": "application/json", "Accept-Encoding": "gzip"}
CLIENT_TIMEOUT = os.getenv("HTTP_CLIENT_TIMEOUT")


class Connection:
    """
    Connection object to hold following connections:
       - Websocket to joern server
       - http connection to joern server
       - http connection to cpggen server
    """

    def __init__(self, cpggenclient, httpclient, websocket):
        self.cpggenclient = cpggenclient
        self.httpclient = httpclient
        self.websocket = websocket

    async def __aenter__(self):
        return self

    async def ping(self):
        """Send websocket ping message"""
        await self.websocket.ping()

    async def close(self):
        """Close all connections"""
        await self.cpggenclient.close()
        await self.httpclient.close()
        await self.websocket.close()

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        return await self.close()


async def get(
    base_url="http://localhost:9000",
    cpggen_url="http://localhost:7072",
    username=None,
    password=None,
):
    """Method to create a connection to joern and cpggen server"""
    auth = None
    if username and password:
        auth = httpx.BasicAuth(username, password)
    base_url = base_url.rstrip("/")
    client = httpx.AsyncClient(base_url=base_url, auth=auth, timeout=CLIENT_TIMEOUT)
    cpggenclient = None
    if cpggen_url:
        cpggenclient = httpx.AsyncClient(base_url=cpggen_url, timeout=CLIENT_TIMEOUT)
    ws_url = f"""{base_url.replace("http://", "ws://").replace("https://", "wss://")}/connect"""
    websocket = await websockets.connect(ws_url, ping_timeout=None)
    connected_msg = await websocket.recv()
    if connected_msg != "connected":
        raise websockets.exceptions.InvalidState(
            "Didn't receive connected message from Joern server"
        )
    # Workaround to fix websockets.exceptions.ConnectionClosedError
    await asyncio.sleep(0)
    return Connection(cpggenclient, client, websocket)


async def send(connection, message):
    """Send message to the joern server via websocket"""
    await connection.websocket.send(message)


async def receive(connection):
    """Receive message from the joern server"""
    return await connection.websocket.recv()


def fix_json(sout):
    """Hacky method to convert the joern stdout string to json"""
    source_sink_mode = False
    try:
        if "defined function source" in sout:
            source_sink_mode = True
            sout = sout.replace("defined function source\n", "")
            sout = sout.replace("defined function sink\n", "")
        else:
            sout = sout.replace(r'"\"', '"').replace(r'\""', '"')
        if ': String = "[' in sout:
            if source_sink_mode:
                sout = (
                    sout.replace(r"\"", '"')
                    .replace('}]}]"', "}]}]")
                    .replace('\\"', '"')
                )
                sout = sout.split(': String = "')[-1]
            else:
                sout = sout.split(': String = "')[-1][-1]
        elif "tree: ListBuffer" in sout:
            sout = sout.split(": String = ")[-1]
            if '"""' in sout:
                sout = sout.replace('"""', "")
            return sout
        elif 'String = """[' in sout:
            tmpA = sout.split("\n")[1:-2]
            sout = "[ " + "\n".join(tmpA) + "]"
        return orjson.loads(sout)
    except Exception:
        return {"response": sout}


def fix_query(query_str):
    """Utility method to convert CPGQL queries to become json friendly"""
    if "\\." in query_str and "\\\\." not in query_str:
        query_str = query_str.replace("\\.", "\\\\.")
    if (query_str.startswith("cpg.") or query_str.startswith("({cpg.")) and (
        ".toJson" not in query_str
        and ".plotDot" not in query_str
        and not query_str.endswith(".p")
        and ".store" not in query_str
        and "def" not in query_str
        and "printCallTree" not in query_str
    ):
        query_str = f"{query_str}.toJsonPretty"
    return query_str


def parse_error(serr):
    """Method to parse joern output and identify friendly error messages"""
    if "No projects loaded" in serr:
        return """ERROR: Import code using import_code api. Usage: await workspace.import_code(connection, directory_name, app_name)"""
    return serr


async def p(connection, query_str, title="", caption=""):
    """Method to print the result as a table"""
    result = await query(connection, query_str)
    print_table(result, title, caption)
    return result


async def q(connection, query_str):
    """Query joern server and optionally print the result as a table if the query ends with .p"""
    if query_str.strip().endswith(".p"):
        query_str = f"{query_str[:-2]}.toJsonPretty"
        return await p(connection, query_str)
    return await query(connection, query_str)


async def query(connection, query_str):
    """Query joern server"""
    client = connection.httpclient
    response = await client.post(
        url="/query", headers=headers, json={"query": fix_query(query_str)}
    )
    if response.status_code == httpx.codes.OK:
        j = response.json()
        res_uuid = j.get("uuid")
        try:
            completed_uuid = await receive(connection)
            if completed_uuid == res_uuid:
                response = await client.get(
                    url=f"/result/{completed_uuid}", headers=headers
                )
                if response.status_code == httpx.codes.OK:
                    j = response.json()
                    sout = j.get("stdout", "")
                    serr = j.get("stderr", "")
                    if sout:
                        return fix_json(sout)
                    return parse_error(serr)
        except Exception:
            return None
    return None


async def bulk_query(connection, query_list):
    """Bulk query joern server"""
    client = connection.httpclient
    websocket = connection.websocket
    uuid_list = []
    response_list = []
    for query_str in query_list:
        response = await client.post(
            url="/query", headers=headers, json={"query": fix_query(query_str)}
        )
        if response.status_code == httpx.codes.OK:
            j = response.json()
            res_uuid = j.get("uuid")
            uuid_list.append(res_uuid)
    async for completed_uuid in websocket:
        if completed_uuid in uuid_list:
            response = await client.get(
                url=f"/result/{completed_uuid}", headers=headers
            )
            if response.status_code == httpx.codes.OK:
                j = response.json()
                sout = j.get("stdout", "")
                serr = j.get("stderr", "")
                if sout:
                    response_list.append(fix_json(sout))
                else:
                    response_list.append({"error": parse_error(serr)})
        if len(response_list) == len(uuid_list):
            return response_list
    return response_list


async def flows(connection, source, sink):
    """Execute reachableByFlows query"""
    return await flowsp(
        connection,
        source,
        sink,
        print_result=True if os.getenv("POLYNOTE_VERSION") else False,
    )


async def flowsp(connection, source, sink, print_result=True):
    """Execute reachableByFlows query and optionally print the result table"""
    results = await bulk_query(
        connection,
        [
            source,
            sink,
            "sink.reachableByFlows(source).p",
        ],
    )
    if print_result and len(results):
        tmpres = results[-1]
        if isinstance(tmpres, dict) and tmpres.get("response"):
            tmpres = tmpres.get("response")
        tmpA = tmpres.split('"""')[1:-1]
        print_md("\n".join([n for n in tmpA if len(n.strip()) > 1]))
    return results


async def df(
    connection,
    source,
    sink,
    print_result=True if os.getenv("POLYNOTE_VERSION") else False,
    filter=None,
    check_labels=check_labels_list,
):
    """
    Execute reachableByFlows query. Optionally accepts filters which could be a raw conditional string or predefined keywords such as skip_control_structures, skip_cfg and skip_checks
    skip_control_structures: This adds a control structure filter `filter(m => m.elements.isControlStructure.size > 0)` to skip flows with control statements such if condition or break
    skip_cfg: This adds a cfg filter `filter(m => m.elements.isCfgNode.size > 0)` to skip flows with control flow graph nodes
    skip_checks: When used with check_labels parameter, this could filter flows containing known validation and sanitization code in the flow. Has a default list.
    """
    filter_str = ""
    if isinstance(check_labels, str):
        check_labels = check_labels.split("|")
    if isinstance(source, dict):
        for k, v in source.items():
            if k in ("parameter", "tag"):
                source = f"""cpg.tag.name("{v}").{k}"""
            elif k in ("method", "call", "annotation"):
                source = f"""cpg.{k}{expand_search_str(v)}"""
    if isinstance(sink, dict):
        for k, v in sink.items():
            if k in ("parameter", "tag"):
                sink = f"""cpg.tag.name("{v}").{k}"""
            elif k in ("method", "call", "annotation"):
                sink = f"""cpg.{k}{expand_search_str(v)}"""
    if not source.startswith("def"):
        source = f"def source = {source}"
    if not sink.startswith("def"):
        sink = f"def sink = {sink}"
    if filter:
        if isinstance(filter, str):
            if filter == "skip_checks":
                filter_str = f""".filter(m => m.elements.code(".*({'|'.join(check_labels)}).*").size == 0)"""
            elif not filter.startswith("."):
                filter_str = f".filter({filter})"
        elif isinstance(filter, list):
            for k in filter:
                if k == "skip_control_structures":
                    filter_str = f"{filter_str}.filter(m => m.elements.isControlStructure.size > 0)"
                elif k == "skip_cfg":
                    filter_str = (
                        f"{filter_str}.filter(m => m.elements.isCfgNode.size > 0)"
                    )
                elif k == "skip_checks":
                    filter_str = f"""{filter_str}.filter(m => m.elements.code(".*({'|'.join(check_labels)}).*").size == 0)"""
                else:
                    filter_str = f"""{filter_str}.filter({k})"""
    results = await query(
        connection,
        f"""
        {source}
        {sink}
        sink.reachableByFlows(source){filter_str}.map(m => (m, m.elements.location.l)).toJson
        """,
    )
    if print_result:
        print_flows(results)
    return results


async def reachableByFlows(connection, source, sink, print_result=False):
    """Execute reachableByFlows query"""
    return await df(connection, source, sink, print_result)


async def create_cpg(connection, src, out_dir, lang):
    """Create CPG using cpggen server"""
    client = connection.cpggenclient
    if not client:
        return {
            "error": "true",
            "message": "No active connection to cpggen server. Pass the cpggen url to the client.get method.",
        }, 500
    # Suppor for url
    url = ""
    if src.startswith("http") or src.startswith("git"):
        url = src
        src = ""
    response = await client.post(
        url="/cpg",
        headers=headers,
        json={"src": src, "url": url, "out_dir": out_dir, "lang": lang},
    )
    return response.json()
