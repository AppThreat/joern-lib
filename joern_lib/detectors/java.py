import re

from joern_lib import client

HTTP_ANNOTATIONS = "org\\.springframework\\.web\\.bind\\.annotation\\..*"

FILTER_ANNOTATIONS = "javax\\.servlet\\.annotation\\.WebFilter"

SOURCE_TYPE_PATTERN = "(?i).*(cloud|framework|data|http|net|socket|io|security|text|xml|json|proto|rpc|java).*"
SOURCE_FILE_PATTERN = "(?i).*(controller|service).*"
SINK_TYPE_PATTERN = "(?i).*(cloud|framework|data|http|net|socket|io|security|text|xml|json|proto|rpc|java).*"


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
                    route_matches = re.search(r'"(/?.)+"', code)
                    if route_matches:
                        annotation_data["routePattern"] = route_matches.group().replace(
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


async def list_unresolved_external_methods(connection):
    return await client.q(
        connection,
        """cpg.method.external.where(_.fullName(".*<unresolved.*")).whereNot(_.name(".*<(operator|init)>.*"))""",
    )


async def list_methods(
    connection,
    modifier="public ",
    include_annotations=True,
    external=False,
    unresolved=True,
):
    external_bool_str = "external" if external else "internal"
    filter_str = '.whereNot(_.name(".*<(operator|init)>.*"))'
    if not unresolved:
        filter_str = f'{filter_str}.whereNot(_.fullName(".*<unresolved.*"))'
    if include_annotations:
        res = await client.q(
            connection,
            f"""cpg.method.{external_bool_str}{filter_str}.code("{modifier}.*").map(m => (m, m.annotation.l))""",
        )
        return expand_annotations(res)
    else:
        return await client.q(
            connection,
            f"""cpg.method.{external_bool_str}{filter_str}.code("{modifier}.*")""",
        )


def get_sources_query(
    pattern=SOURCE_TYPE_PATTERN,
    file_pattern=SOURCE_FILE_PATTERN,
    parameter_filter='typeFullName("java.lang.String")',
):
    if parameter_filter and not parameter_filter.startswith("."):
        parameter_filter = f".{parameter_filter}"
    return f"""
        (cpg.method.internal.where(_.annotation.fullName("{pattern}")).whereNot(_.fullName(".*<unresolved.*")).whereNot(_.name(".*<(operator|init)>.*")).parameter{parameter_filter} ++ cpg.method.internal.where(_.filename("{file_pattern}")).whereNot(_.fullName(".*<unresolved.*")).whereNot(_.name(".*<(operator|init)>.*")).parameter{parameter_filter}).location.toJson
        """


async def list_sources(
    connection,
    pattern=SOURCE_TYPE_PATTERN,
    file_pattern=SOURCE_FILE_PATTERN,
    parameter_filter='typeFullName("java.lang.String")',
):
    if parameter_filter and not parameter_filter.startswith("."):
        parameter_filter = f".{parameter_filter}"
    return await client.q(
        connection,
        get_sources_query(
            pattern=pattern,
            file_pattern=file_pattern,
            parameter_filter=parameter_filter,
        ),
    )


def get_sinks_query(pattern=SINK_TYPE_PATTERN):
    return f'cpg.method.external.where(_.fullName("{pattern}")).whereNot(_.fullName(".*<unresolved.*")).whereNot(_.name(".*<(operator|init)>.*")).whereNot(_.signature("boolean.*")).parameter.location'


async def list_sinks(connection, pattern=SINK_TYPE_PATTERN):
    return await client.q(connection, get_sinks_query(pattern=pattern))


async def suggest_flows(
    connection,
):
    return await client.df(
        connection,
        get_sources_query().replace(".location.toJson", ""),
        get_sinks_query().replace(".location", ""),
    )
