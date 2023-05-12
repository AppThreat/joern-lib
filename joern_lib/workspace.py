import json
import os

from joern_lib import client


def extract_dir(res):
    if res.get("response"):
        dir_name = res.get("response").split('String = "')[-1].split('"')[0]
        return dir_name
    return None


async def ls(connection):
    res = await client.q(connection, "workspace")
    if "[io.joern.joerncli.console.JoernProject] = empty" in res.get("response", ""):
        return None
    return res.get("response")


async def slice_cpg(
    connection,
    src,
    out_dir=None,
    languages="autodetect",
    project_name=None,
):
    app_manifests = await create_cpg(
        connection,
        src,
        out_dir=out_dir,
        languages=languages,
        project_name=project_name,
        slice=True,
        slice_mode="Usages",
    )
    if not app_manifests:
        return None
    if isinstance(app_manifests, (list, tuple)):
        app_manifests = app_manifests[0]
    if app_manifests.get("slice_out") and os.path.exists(
        app_manifests.get("slice_out")
    ):
        try:
            with open(app_manifests.get("slice_out")) as fp:
                return json.load(fp)
        except Exception:
            return None
    return None


async def create_cpg(
    connection,
    src,
    out_dir=None,
    languages="autodetect",
    project_name=None,
    slice=None,
    slice_mode="Usages",
):
    app_manifests = []
    res = await client.create_cpg(
        connection,
        src,
        out_dir=out_dir,
        lang=languages,
        slice=slice,
        slice_mode=slice_mode,
    )
    if res:
        app_manifests = res.get("app_manifests", [])
        if app_manifests:
            first_app = app_manifests[0]
            if not project_name and first_app.get("app"):
                project_name = first_app.get("app")
            cpg_path = first_app.get("cpg")
            res = await import_cpg(connection, cpg_path, project_name)
            if not res:
                return None
    return (
        app_manifests[0] if app_manifests and len(app_manifests) == 1 else app_manifests
    )


async def import_cpg(connection, cpg_path, project_name=None):
    if cpg_path:
        res = await dir_exists(connection, cpg_path)
        if not res:
            raise ValueError(
                f"CPG {cpg_path} doesn't exist for import into Joern. Check if the directory containing this CPG is mounted and accessible from the server."
            )
    if project_name:
        res = await client.q(
            connection, f"""importCpg("{cpg_path}", "{project_name}")"""
        )
    else:
        res = await client.q(connection, f"""importCpg("{cpg_path}")""")
    if isinstance(res, str):
        return False
    if "The graph has been modified" in res.get("response", ""):
        # Execute save command
        await client.q(connection, "save")
        return True
    return False


async def import_code(connection, directory, project_name=None):
    if directory:
        res = await dir_exists(connection, directory)
        if not res:
            raise ValueError(
                f"Directory {directory} doesn't exist for import into Joern. Check if the directory is mounted and accessible from the server."
            )
    if project_name:
        res = await client.q(
            connection, f"""importCode("{directory}", "{project_name}")"""
        )
    else:
        res = await client.q(connection, f"""importCode("{directory}")""")
    if isinstance(res, str):
        return False
    if "Code successfully imported" in res.get("response", ""):
        # Execute save command
        await client.q(connection, "save")
        return True
    return False


async def from_string(connection, code_snippet, language="jssrc"):
    res = await client.q(
        connection, f'importCode.{language}.fromString("""{code_snippet}""")'
    )
    if isinstance(res, str):
        return False
    if res and "Code successfully imported" in res.get("response", ""):
        return True
    return False


async def reset(connection):
    await client.q(connection, "workspace.reset")
    return True


async def get_path(connection):
    res = await client.q(connection, "workspace.getPath")
    return extract_dir(res)


async def get_active_project(connection):
    return await client.q(connection, "workspace.getActiveProject")


async def set_active_project(connection, project_name):
    res = await client.q(
        connection, f"""workspace.setActiveProject("{project_name}")"""
    )
    if isinstance(res, str):
        return False
    if res and "projectFile = ProjectFile(inputPath =" in res.get("response", ""):
        return True
    return False


async def delete_project(connection, project_name):
    return await client.q(connection, f"""workspace.deleteProject("{project_name}")""")


async def cpg_exists(connection, project_name):
    if project_name:
        res = await client.q(connection, f"""workspace.cpgExists("{project_name}")""")
        if res and "Boolean = true" in res.get("response", ""):
            return True
    return False


async def get_overlay_dir(connection, project_name):
    res = await client.q(
        connection, f"""workspace.overlayDirByProjectName("{project_name}")"""
    )
    return extract_dir(res)


async def dir_exists(connection, dir_name):
    res = await client.q(connection, f"""os.exists(os.Path("{dir_name}"))""")
    if res and "Boolean = true" in res.get("response", ""):
        return True
    return False
