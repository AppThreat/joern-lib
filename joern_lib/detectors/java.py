import re

from joern_lib import client

HTTP_ANNOTATIONS = "org\\.springframework\\.web\\.bind\\.annotation\\..*"

FILTER_ANNOTATIONS = "javax\\.servlet\\.annotation\\.WebFilter"


def expand_annotations(rows):
    ret_rows = []
    for r in rows:
        m = {}
        if not r or not isinstance(r, dict):
            continue
        if r.get("_1"):
            method_data = r.get("_1")
            for k, v in method_data.items():
                m[k] = v
        if r.get("_2"):
            annotation_list = r.get("_2")
            mannotation_list = []
            for annotation_data in annotation_list:
                http_method = ""
                if annotation_data.get("_label") == "ANNOTATION":
                    if (
                        "org.springframework.web.bind.annotation"
                        in annotation_data.get("fullName")
                    ):
                        http_method = (
                            annotation_data.get("name").replace("Mapping", "").upper()
                        )
                        annotation_data["httpMethod"] = http_method
                    code = annotation_data.get("code")
                    routeMatches = re.search(r'"(\/?.)+"', code)
                    if routeMatches:
                        annotation_data["routePattern"] = routeMatches.group().replace(
                            '"', ""
                        )
                mannotation_list.append(annotation_data)
            if mannotation_list:
                m["annotation"] = (
                    mannotation_list[0]
                    if len(mannotation_list) == 1
                    else mannotation_list
                )
        ret_rows.append(m)
    return ret_rows


async def list_http_routes(connection, annotations=HTTP_ANNOTATIONS):
    res = await client.q(
        connection,
        f"""cpg.method.internal.where(_.annotation.fullName("{annotations}")).map(m => (m, m.annotation.l))""",
    )
    return expand_annotations(res)


async def list_http_filters(connection, annotations=FILTER_ANNOTATIONS):
    res = await client.q(
        connection,
        f"""cpg.typeDecl.where(_.annotation.fullName("{annotations}")).map(m => (m, m.annotation.l))""",
    )
    return expand_annotations(res)


async def list_methods(
    connection, modifier="public ", include_annotations=True, external=False
):
    external_bool_str = "true" if external else "false"
    if include_annotations:
        res = await client.q(
            connection,
            f"""cpg.method.isExternal({external_bool_str}).code("{modifier}.*").map(m => (m, m.annotation.l))""",
        )
        return expand_annotations(res)
    else:
        return await client.q(
            connection,
            f"""cpg.method.isExternal({external_bool_str}).code("{modifier}.*")""",
        )
