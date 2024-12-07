from logging import getLogger
from typing import Optional, Type, Union

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
        return_type: Optional[Type] = str,
        default: Optional[Union[bool, int, str]] = None,
    ):
        res = self.config.get(name, default)
        if is_required and (
            res is None or (isinstance(res, str) and res.strip() == "")
        ):
            LOGGER.error(f"Config {name} not found, Exiting..")
            exit()
        try:
            if return_type is not None and res is not None:
                res = return_type(res)
        except ValueError as e:
            LOGGER.error(f"Error converting {name} to {return_type.__name__}: {e}")
            exit()
        return res
