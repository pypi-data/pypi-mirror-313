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

"""Pasty Library"""

import requests

PASTE_URL = "https://pasty.lus.pm"


def paste_content(content: str):
    data = {
        "content": content,
    }
    re = requests.post(url=f"{PASTE_URL}/api/v2/pastes", json=data)
    data = re.json()
    return {
        "url": f"{PASTE_URL}/{data['id']}",
        "raw": f"{PASTE_URL}/{data['id']}/raw",
        "modificationToken": data["modificationToken"],
    }


def get_content(paste_id: str):
    re = requests.get(url=f"{PASTE_URL}/api/v2/pastes/{paste_id}")
    data = re.json()
    return {
        "url": f"{PASTE_URL}/{data['id']}",
        "content": data["content"],
        "created": data["created"],
    }
