from joern_lib import client
from joern_lib.utils import expand_search_str


async def list_files(connection, search_descriptor=None):
    search_str = expand_search_str(search_descriptor)
    return await client.q(connection, f"cpg.file{search_str}")


async def list_annotations(connection):
    return await client.q(connection, "cpg.annotation")


async def list_arguments(connection):
    return await client.q(connection, "cpg.argument")


async def list_assignments(connection):
    return await client.q(connection, "cpg.assignment")


async def list_calls(connection, search_descriptor=None):
    search_str = expand_search_str(search_descriptor)
    return await client.q(connection, f"cpg.call{search_str}")


async def list_config_files(connection):
    return await client.q(connection, "cpg.configFile")


async def list_control_structures(connection):
    return await client.q(connection, "cpg.controlStructure")


async def list_dependencies(connection):
    return await client.q(connection, "cpg.dependency")


async def list_identifiers(connection):
    return await client.q(connection, "cpg.identifier")


async def list_declared_identifiers(connection):
    return await client.q(
        connection,
        """({cpg.assignment.argument(1).isIdentifier.refsTo ++ cpg.parameter.filter(_.typeFullName != "ANY")})""",
    )


async def list_imports(connection):
    return await client.q(connection, "cpg.imports")


async def list_if_blocks(connection):
    return await client.q(connection, "cpg.ifBlock")


async def list_literals(connection):
    return await client.q(connection, "cpg.literal")


async def list_locals(connection):
    return await client.q(connection, "cpg.local")


async def list_members(connection):
    return await client.q(connection, "cpg.member")


async def list_metadatas(connection):
    return await client.q(connection, "cpg.metaData")


async def list_methods(connection, search_descriptor=None, skip_operators=True):
    search_str = expand_search_str(search_descriptor)
    filter_str = ""
    if skip_operators:
        filter_str = '.whereNot(_.name(".*<operator>.*"))'

    return await client.q(connection, f"""cpg.method{search_str}{filter_str}""")


async def list_constructors(connection):
    return await client.q(connection, """cpg.method.internal.name("<init>")""")


async def list_external_methods(connection):
    return await client.q(
        connection, """cpg.method.isExternal(true).whereNot(_.name(".*<operator>.*"))"""
    )


async def list_method_refs(connection):
    return await client.q(connection, "cpg.methodRef")


async def list_methodReturns(connection):
    return await client.q(connection, "cpg.methodReturn")


async def list_namespaces(connection):
    return await client.q(connection, "cpg.namespace")


async def list_parameters(connection):
    return await client.q(connection, "cpg.parameter")


async def list_tags(
    connection,
    name=None,
    value=None,
    is_call=False,
    is_method=False,
    is_parameter=False,
):
    suffix = ""
    if is_call:
        suffix = ".call"
    elif is_method:
        suffix = ".method"
    elif is_parameter:
        suffix = ".parameter"
    if name:
        return await client.q(connection, f"""cpg.tag.name("{name}"){suffix}""")
    elif value:
        return await client.q(connection, f"""cpg.tag.value("{value}"){suffix}""")
    return await client.q(connection, "cpg.tag{suffix}")


async def create_tags(connection, query=None, call=None, method=None, tags=[]):
    """
    Method to create custom tags on nodes. Nodes could be selected based on a query, or call or method name.

    Tags could be a list of string or dictionary of key, value pairs
    """
    if not query and call:
        query = f"""cpg.call.name("{call}")"""
    elif not query and method:
        query = f"""cpg.method.name("{method}")"""
    if query and tags:
        for tag in tags:
            if isinstance(tag, dict):
                for k, v in tag.items():
                    await client.q(
                        connection,
                        f"""
                        {query}.newTagNodePair("{k}", "{v}").store
                        run.commit
                        save
                        """,
                    )
            if isinstance(tag, str):
                await client.q(
                    connection,
                    f"""
                {query}.newTagNode("{tag}").store
                run.commit
                save
                """,
                )


async def list_types(connection):
    return await client.q(connection, "cpg.typ")


async def list_custom_types(connection):
    return await client.q(
        connection,
        """cpg.typeDecl.filterNot(t => t.isExternal || t.name.matches("(:program|<module>|<init>|<meta>|<body>)"))""",
    )


async def get_calls(connection, pattern):
    return await client.q(connection, f"""cpg.call.code("(?i){pattern}")""")


async def get_method_callIn(connection, pattern):
    return await client.q(
        connection, f"""cpg.method("(?i){pattern}").callIn.location"""
    )


async def get_identifiers_in_file(connection, filename):
    return await client.q(
        connection,
        f"""cpg.call.name(Operators.assignment).argument.order(1).map(t => (t, t.location.filename)).filter(_._2.equals("{filename}")).filter(_._1.isIdentifier).map(_._1.code).filterNot(_.contains("_tmp_")).dedup""",
    )


async def get_methods_multiple_returns(connection):
    return await get_functions_multiple_returns(connection)


async def get_functions_multiple_returns(connection):
    return await client.q(
        connection,
        """({cpg.method.internal.filter(_.ast.isReturn.l.size > 1).nameNot("<global>")}).location""",
    )


async def get_complex_methods(connection, n=4):
    return await get_complex_functions(connection, n)


async def get_complex_functions(connection, n=4):
    return await client.q(
        connection,
        """({cpg.method.internal.filter(_.controlStructure.size > %(n)d).nameNot("<global>")}).location"""
        % dict(n=n),
    )


async def get_long_methods(connection, n=1000):
    return await get_long_functions(connection, n)


async def get_long_functions(connection, n=1000):
    return await client.q(
        connection,
        """({cpg.method.internal.filter(_.numberOfLines > %(n)d).nameNot("<global>")}).location"""
        % dict(n=n),
    )


async def get_too_many_loops_methods(connection, n=4):
    return await get_too_many_loops_functions(connection, n)


async def get_too_many_loops_functions(connection, n=4):
    return await client.q(
        connection,
        """({cpg.method.internal.filter(_.ast.isControlStructure.controlStructureType("(FOR|DO|WHILE)").size > %(n)d).nameNot("<global>")}).location"""
        % dict(n=n),
    )


async def get_too_many_params_methods(connection, n=4):
    return await get_too_many_params_functions(connection, n)


async def get_too_many_params_functions(connection, n=4):
    return await client.q(
        connection,
        """({cpg.method.internal.filter(_.parameter.size > %(n)d).nameNot("<global>")}).location"""
        % dict(n=n),
    )


async def get_too_nested_methods(connection, n=4):
    return await get_too_nested_functions(connection, n)


async def get_too_nested_functions(connection, n=4):
    return await client.q(
        connection,
        """({cpg.method.internal.filter(_.depth(_.isControlStructure) > %(n)d).nameNot("<global>")}).location"""
        % dict(n=n),
    )


async def get_call_tree(connection, method_name, n=3):
    await client.q(
        connection,
        """
import scala.collection.mutable.ListBuffer
def printDashes(count: Int) = {
    var tabStr = "+--- "
    var i = 0
    while (i < count) {
        tabStr = "|    " + tabStr
        i += 1
    }
    tabStr
}
def printCallTree(callerFullName : String, tree: ListBuffer[String], depth: Int) {
    var dashCount = 0
    var lastCallerMethod = callerFullName
    var lastDashCount = 0
    tree += callerFullName
    def findCallee(methodName: String, tree: ListBuffer[String]) {
        var calleeList = cpg.method.fullNameExact(methodName).callee.whereNot(_.name(".*<operator>.*")).l
        var callerNameList = cpg.method.fullNameExact(methodName).caller.fullName.l
        if (callerNameList.contains(lastCallerMethod) || (callerNameList.size == 0)) {
            dashCount = lastDashCount
        } else {
            lastDashCount = dashCount
            lastCallerMethod = methodName
            dashCount += 1
        }
        if (dashCount < depth) {
            calleeList foreach { c =>
                tree += printDashes(dashCount) + c.fullName
                findCallee(c.fullName, tree)
            }
        }
    }
    findCallee(lastCallerMethod, tree)
}
""",
    )
    return await client.q(
        connection,
        """
        var tree = new ListBuffer[String]()
        printCallTree("%(method_name)s", tree, %(n)d)
        tree.toList.mkString("\\n")
        """
        % dict(method_name=method_name, n=n),
    )
