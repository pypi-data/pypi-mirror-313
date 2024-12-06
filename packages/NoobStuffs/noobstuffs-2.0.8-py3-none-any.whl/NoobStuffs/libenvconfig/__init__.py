from logging import getLogger
from os import getenv
from typing import Optional, Union

LOGGER = getLogger("EnvConfig")


def getConfig(
    name: str,
    is_required: bool = False,
    return_type: str = "str",
    default: Optional[Union[bool, int, str]] = None,
):
    res = getenv(name, default)
    if is_required and (not res or (isinstance(res, str) and res.strip() == "")):
        LOGGER.error(f"Config {name} not found, Exiting..")
        exit()
    if return_type == "str" or return_type == None:
        pass
    elif return_type == "int":
        res = int(res)
    elif return_type == "bool":
        res = str(res).lower() == "true"
    else:
        LOGGER.error("Invalid return type value, only use (str | int | bool | None)")
        exit()
    return res
