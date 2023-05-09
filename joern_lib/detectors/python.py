import re

from joern_lib import client

ROUTE_DECORATORS = "route"


async def list_decorator_location(connection, decorator, is_method_ref=True):
    """
    Method to list the methods and their location for a given decorator
    """
    method_ref_filter = ".isMethodRef" if is_method_ref else ""
    return await client.q(
        connection,
        f'cpg.call.code(".*{decorator}.*").inCall.assignment.argument{method_ref_filter}.location',
    )


async def list_dict_assignment_location(connection, key=None, is_literal=True):
    """
    Method to list locations where a dictionary key is assigned a hardcoded value
    """
    code_filter = f'.code(".*{key}.*")' if key else ""
    literal_filter = ".isLiteral" if is_literal else ""
    return await client.q(
        connection,
        f"cpg.call(Operators.indexAccess){code_filter}.inCall.assignment.argument{literal_filter}.location",
    )


def expand_decorators(rows):
    ret_rows = []
    for row in rows:
        m = {}
        ann = {}
        if not row or not isinstance(row, dict):
            continue
        if row.get("_1"):
            decorator_data = row.get("_1")
            for k, v in decorator_data.items():
                ann[k] = v
                if k == "code":
                    routeMatches = re.search(r'"(\/?.[^,\s()])+"', v)
                    if routeMatches.group():
                        ann["routePattern"] = routeMatches.group().replace('"', "")
                        for hm in ("GET", "DELETE", "PUT", "POST", "PATCH", "OPTION"):
                            if hm in v:
                                ann["httpMethod"] = hm
            m["annotation"] = ann
        if row.get("_2"):
            method_data = row.get("_2")
            for k, v in method_data.items():
                m[k] = v
        ret_rows.append(m)
    return ret_rows


async def list_http_routes(connection, decorators=ROUTE_DECORATORS):
    res = await client.q(
        connection,
        f"""cpg.call.code(".*{decorators}.*").inCall.assignment.map(m => (m, m.method))""",
    )
    return expand_decorators(res)
