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

from logging import getLogger
from random import choices
from string import ascii_letters
from time import sleep

from telegraph import Telegraph
from telegraph.exceptions import RetryAfterError

LOGGER = getLogger("TelegraphHelper")


class TelegraphHelper:
    def __init__(
        self,
        author_name: str,
        author_url: str,
        domain: str = "telegra.ph",
    ):
        self.telegraph = Telegraph(domain=domain)
        self.short_name = "".join(choices(population=ascii_letters, k=5))
        self.author_name = author_name
        self.author_url = author_url
        self.create_account()

    def create_account(self):
        LOGGER.info(f"Creating account: {self.author_name}")
        self.telegraph.create_account(
            short_name=self.short_name,
            author_name=self.author_name,
            author_url=self.author_url,
        )

    def create_page(self, title: str, content: str):
        LOGGER.info(f"Creating page: {title}")
        try:
            return self.telegraph.create_page(
                title=title,
                html_content=content,
                author_name=self.author_name,
                author_url=self.author_url,
            )
        except RetryAfterError as err:
            LOGGER.error(
                f"Telegraph Flood control exceeded, sleeping for {err.retry_after} seconds.",
            )
            sleep(err.retry_after)
            return self.create_page(title, content)

    def upload_file(self, path: str):
        LOGGER.info(f"Uploading file: {path}")
        try:
            return self.telegraph.upload_file(path)
        except RetryAfterError as err:
            LOGGER.error(
                f"Telegraph Flood control exceeded, sleeping for {err.retry_after} seconds.",
            )
            sleep(err.retry_after)
            return self.upload_file(path)
