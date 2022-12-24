import asyncio
import uvloop
import orjson
import signal

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import httpx
import websockets

headers = {"Content-Type": "application/json", "Accept-Encoding": "gzip"}


class Connection:
    def __init__(self, httpclient, websocket):
        self.httpclient = httpclient
        self.websocket = websocket
        # Close the connection when receiving SIGTERM.
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(
            signal.SIGTERM, loop.create_task, self.websocket.close()
        )

    async def ping(self):
        await self.websocket.ping()

    async def close(self):
        await self.httpclient.close()
        await self.websocket.close()


async def get(base_url, username=None, password=None):
    auth = None
    if username and password:
        auth = httpx.BasicAuth(username, password)
    base_url = base_url.rstrip("/")
    client = httpx.AsyncClient(base_url=base_url, auth=auth)
    ws_url = f"""{base_url.replace("http://", "ws://").replace("https://", "wss://")}/connect"""
    websocket = await websockets.connect(ws_url, ping_timeout=None)
    connected_msg = await websocket.recv()
    if connected_msg != "connected":
        raise websockets.exceptions.InvalidState(
            "Didn't receive connected message from Joern server"
        )
    return Connection(client, websocket)


async def send(connection, message):
    await connection.websocket.send(message)


async def receive(connection):
    return await connection.websocket.recv()


def fix_json(sout):
    try:
        if ': String = "[' in sout:
            sout = sout.split(': String = "')[-1][-1]
        elif 'String = """[' in sout:
            tmpA = sout.split("\n")[1:-2]
            sout = "[ " + "\n".join(tmpA) + "]"
        return orjson.loads(sout)
    except Exception as e:
        return {"response": sout}


def fix_query(query):
    if "\\." in query and "\\\\." not in query:
        query = query.replace("\\.", "\\\\.")
    if query.startswith("cpg.") and ".toJson" not in query:
        query = f"{query}.toJsonPretty"
    return query


def parse_error(serr):
    if "No projects loaded" in serr:
        return """ERROR: Import code using import_code api. Usage: await workspace.import_code(connection, directory_name, app_name)"""
    return serr


async def query(connection, query):
    client = connection.httpclient
    response = await client.post(
        url="/query", headers=headers, json={"query": fix_query(query)}
    )
    if response.status_code == httpx.codes.OK:
        j = response.json()
        res_uuid = j.get("uuid")
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
    return None


async def bulk_query(connection, query_list):
    client = connection.httpclient
    websocket = connection.websocket
    uuid_list = []
    response_list = []
    for query in query_list:
        response = await client.post(
            url="/query", headers=headers, json={"query": fix_query(query)}
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
