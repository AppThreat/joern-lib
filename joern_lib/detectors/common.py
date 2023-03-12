from joern_lib import client


async def list_files(connection):
    return await client.q(connection, "cpg.file")


async def list_annotations(connection):
    return await client.q(connection, "cpg.annotation")


async def list_arguments(connection):
    return await client.q(connection, "cpg.argument")


async def list_assignments(connection):
    return await client.q(connection, "cpg.assignment")


async def list_calls(connection):
    return await client.q(connection, "cpg.call")


async def list_config_files(connection):
    return await client.q(connection, "cpg.configFile")


async def list_control_structures(connection):
    return await client.q(connection, "cpg.controlStructure")


async def list_dependencies(connection):
    return await client.q(connection, "cpg.dependency")


async def list_identifiers(connection):
    return await client.q(connection, "cpg.identifier")


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


async def list_methods(connection):
    return await client.q(connection, "cpg.method")


async def list_method_refs(connection):
    return await client.q(connection, "cpg.methodRef")


async def list_methodReturns(connection):
    return await client.q(connection, "cpg.methodReturn")


async def list_namespaces(connection):
    return await client.q(connection, "cpg.namespace")


async def list_parameters(connection):
    return await client.q(connection, "cpg.parameter")


async def list_tags(connection):
    return await client.q(connection, "cpg.tag")


async def list_types(connection):
    return await client.q(connection, "cpg.typ")


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


async def get_functions_multiple_returns(connection):
    return await client.q(
        connection,
        """({cpg.method.internal.filter(_.ast.isReturn.l.size > 1).nameNot("<global>")}).location""",
    )


async def get_complex_functions(connection, n=4):
    return await client.q(
        connection,
        """({cpg.method.internal.filter(_.controlStructure.size > %(n)d).nameNot("<global>")}).location"""
        % dict(n=n),
    )


async def get_long_functions(connection, n=1000):
    return await client.q(
        connection,
        """({cpg.method.internal.filter(_.numberOfLines > %(n)d).nameNot("<global>")}).location"""
        % dict(n=n),
    )


async def get_too_many_loops_functions(connection, n=4):
    return await client.q(
        connection,
        """({cpg.method.internal.filter(_.ast.isControlStructure.controlStructureType("(FOR|DO|WHILE)").size > %(n)d).nameNot("<global>")}).location"""
        % dict(n=n),
    )


async def get_too_many_params_functions(connection, n=4):
    return await client.q(
        connection,
        """({cpg.method.internal.filter(_.parameter.size > %(n)d).nameNot("<global>")}).location"""
        % dict(n=n),
    )


async def get_too_nested_functions(connection, n=4):
    return await client.q(
        connection,
        """({cpg.method.internal.filter(_.depth(_.isControlStructure) > %(n)d).nameNot("<global>")}).location"""
        % dict(n=n),
    )
