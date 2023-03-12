from joern_lib.detectors.common import get_method_callIn


async def get_gets(connection):
    return await get_method_callIn(connection, "gets")


async def get_getwd(connection):
    return await get_method_callIn(connection, "getwd")


async def get_scanf(connection):
    return await get_method_callIn(connection, "scanf")


async def get_strcat(connection):
    return await get_method_callIn(connection, "(strcat|strncat)")


async def get_strcpy(connection):
    return await get_method_callIn(connection, "(strcpy|strncpy)")


async def get_strtok(connection):
    return await get_method_callIn(connection, "strtok")
