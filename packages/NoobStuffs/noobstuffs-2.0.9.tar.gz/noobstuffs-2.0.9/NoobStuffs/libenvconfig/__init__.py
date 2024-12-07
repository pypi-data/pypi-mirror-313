from logging import getLogger
from os import getenv
from typing import Optional, Type, Union

LOGGER = getLogger("EnvConfig")


def getConfig(
    name: str,
    is_required: bool = False,
    return_type: Optional[Type] = str,
    default: Optional[Union[bool, int, str]] = None,
):
    res = getenv(name, default)
    if is_required and (res is None or (isinstance(res, str) and res.strip() == "")):
        LOGGER.error(f"Config {name} not found, Exiting..")
        exit()
    try:
        if return_type is not None and res is not None:
            res = return_type(res)
    except ValueError as e:
        LOGGER.error(f"Error converting {name} to {return_type.__name__}: {e}")
        exit()
    return res
