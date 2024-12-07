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

import string

import requests

MAGISK_DICT = {
    "Stable": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/stable.json",
    "Beta": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/beta.json",
    "Canary": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/canary.json",
}


def get_magisk(version_type: str):
    if string.capwords(version_type) in list(MAGISK_DICT.keys()):
        data = requests.get(url=MAGISK_DICT[string.capwords(version_type)]).json()
        return {
            "type": string.capwords(version_type),
            "version": data["magisk"]["version"],
            "download": data["magisk"]["link"],
            "changelog": data["magisk"]["note"],
        }
    else:
        raise Exception("Oh noo you gave wrong version type.")


def get_all_magisks():
    releases = dict()
    for name, release_url in MAGISK_DICT.items():
        data = requests.get(release_url).json()
        releases.update(
            {
                name: {
                    "version": data["magisk"]["version"],
                    "download": data["magisk"]["link"],
                    "changelog": data["magisk"]["note"],
                },
            },
        )
    return releases
