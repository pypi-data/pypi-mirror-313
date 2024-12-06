from logging import getLogger
from typing import Optional, Union

import yaml

LOGGER = getLogger("YAMLConfig")


class YAMLConfig:
    def __init__(self, file_path: str):
        try:
            with open(file_path) as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError:
            LOGGER.error(f"Config file {file_path} not found.")
            exit()
        except yaml.YAMLError as e:
            LOGGER.error(f"Error while parsing YAML file: {e}")
            exit()

    def getConfig(
        self,
        name: str,
        is_required: bool = False,
        return_type: str = "str",
        default: Optional[Union[bool, int, str]] = None,
    ):
        res = self.config.get(name, default)
        if is_required and (not res or (isinstance(res, str) and res.strip() == "")):
            LOGGER.error(f"Config {name} not found, Exiting..")
            exit()
        if return_type == "str" or return_type is None:
            pass
        elif return_type == "int":
            res = int(res)
        elif return_type == "bool":
            res = str(res).lower() == "true"
        else:
            LOGGER.error(
                "Invalid return type value, only use (str | int | bool | None)",
            )
            exit()
        return res
