#
# Copyright (c) 2022 PrajjuS <theprajjus@gmail.com>.
#
# This file is part of NoobStuffs
# (see http://github.com/PrajjuS/NoobStuffs).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""Logging Library"""

import logging

STREAM_FORMAT = "[%(levelname)s] - %(name)s: %(message)s"
LOG_FORMAT = "[%(levelname)s] [%(asctime)s] - %(name)s: %(message)s"
VERBOSE_FORMAT = "[%(levelname)s] [%(asctime)s] [%(filename)s %(lineno)d] %(funcName)s - %(name)s: %(message)s"


def setup_logging(name: str, verbose: bool = False):
    if verbose:
        stream_formatter = logging.Formatter(STREAM_FORMAT)
        file_formatter = logging.Formatter(LOG_FORMAT)
        verbose_formatter = logging.Formatter(VERBOSE_FORMAT)
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(f"{name}.log")
        verbose_handler = logging.FileHandler(f"{name}-DEBUG.log")
        stream_handler.setFormatter(stream_formatter)
        file_handler.setFormatter(file_formatter)
        verbose_handler.setFormatter(verbose_formatter)
        stream_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        verbose_handler.setLevel(logging.DEBUG)
        logging.basicConfig(
            handlers=[stream_handler, file_handler, verbose_handler],
            level=logging.DEBUG,
        )
        logger = logging.getLogger(name=name)
    else:
        stream_formatter = logging.Formatter(STREAM_FORMAT)
        file_formatter = logging.Formatter(LOG_FORMAT)
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(f"{name}.log")
        stream_handler.setFormatter(stream_formatter)
        file_handler.setFormatter(file_formatter)
        stream_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        logging.basicConfig(handlers=[stream_handler, file_handler], level=logging.INFO)
        logger = logging.getLogger(name=name)
    return logger
