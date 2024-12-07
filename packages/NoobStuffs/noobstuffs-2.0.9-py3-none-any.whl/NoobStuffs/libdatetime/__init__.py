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

"""Date Time Library"""

import datetime
from typing import Optional

import pytz

TIME_FORMAT = "%H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
DAY_FORMAT = "%A"


def dtnow(tzinfo: str = "Asia/Kolkata"):
    dt = datetime.datetime.now(pytz.timezone(tzinfo))
    TIME = dt.strftime(TIME_FORMAT)
    DATE = dt.strftime(DATE_FORMAT)
    DAY = dt.strftime(DAY_FORMAT)
    return {
        "time": TIME,
        "date": DATE,
        "day": DAY,
    }


def fromtimestamp(timestamp: int, tzinfo: Optional[str] = None):
    if tzinfo == None:
        dt = datetime.datetime.fromtimestamp(timestamp)
    else:
        dt = datetime.datetime.fromtimestamp(timestamp, pytz.timezone(tzinfo))
    TIME = dt.strftime(TIME_FORMAT)
    DATE = dt.strftime(DATE_FORMAT)
    DAY = dt.strftime(DAY_FORMAT)
    return {
        "time": TIME,
        "date": DATE,
        "day": DAY,
    }


def fromdatetime(date_time: str, dtformat: str):
    dt = datetime.datetime.strptime(date_time, dtformat)
    return dt.timestamp()
