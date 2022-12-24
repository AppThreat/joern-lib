from joern_lib import client


async def list_files(connection):
    return await client.query(connection, "cpg.file")


async def list_annotations(connection):
    return await client.query(connection, "cpg.annotation")


async def list_arguments(connection):
    return await client.query(connection, "cpg.argument")


async def list_assignments(connection):
    return await client.query(connection, "cpg.assignment")


async def list_calls(connection):
    return await client.query(connection, "cpg.call")


async def list_config_files(connection):
    return await client.query(connection, "cpg.configFile")


async def list_control_structures(connection):
    return await client.query(connection, "cpg.controlStructure")


async def list_dependencies(connection):
    return await client.query(connection, "cpg.dependency")


async def list_identifiers(connection):
    return await client.query(connection, "cpg.identifier")


async def list_imports(connection):
    return await client.query(connection, "cpg.imports")


async def list_if_blocks(connection):
    return await client.query(connection, "cpg.ifBlock")


async def list_literals(connection):
    return await client.query(connection, "cpg.literal")


async def list_locals(connection):
    return await client.query(connection, "cpg.local")


async def list_members(connection):
    return await client.query(connection, "cpg.member")


async def list_metadatas(connection):
    return await client.query(connection, "cpg.metaData")


async def list_methods(connection):
    return await client.query(connection, "cpg.method")


async def list_method_refs(connection):
    return await client.query(connection, "cpg.methodRef")


async def list_methodReturns(connection):
    return await client.query(connection, "cpg.methodReturn")


async def list_namespaces(connection):
    return await client.query(connection, "cpg.namespace")


async def list_parameters(connection):
    return await client.query(connection, "cpg.parameter")


async def list_tags(connection):
    return await client.query(connection, "cpg.tag")


async def list_types(connection):
    return await client.query(connection, "cpg.typ")


async def get_calls(connection, pattern):
    return await client.query(connection, f"""cpg.call.code("{pattern}")""")
