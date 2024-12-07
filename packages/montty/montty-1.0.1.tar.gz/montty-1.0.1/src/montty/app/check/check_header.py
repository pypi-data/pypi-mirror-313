# MIT License
#
# Copyright (c) 2024 Gwyn Davies
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR,
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from montty.app.status import Status
from montty.app.check.check_level import CheckLevel
from montty.platform.config_values import ConfigValues


class CheckHeader():
    def __init__(self, title: str, status: Status, check_level: CheckLevel):
        if not title:
            raise Exception(
                "Check header title cannot be empty")
        if len(title) > ConfigValues.CHECK_MAX_HEADER_TITLE_LENGTH:
            print(
                f"Check header title length, must be <= {ConfigValues.CHECK_MAX_HEADER_TITLE_LENGTH} chars long - TRUNCATING', given {title} of {len(title)}")
            # Truncate the title, and add '**' to the end to visually indicate truncation
            self._title: str = title[:ConfigValues.CHECK_MAX_HEADER_TITLE_LENGTH-2] + '**'
        else:
            self._title: str = title

        if not status:
            raise Exception(
                "Check header status cannot be empty")
        self._status: Status = status

        if not check_level:
            raise Exception(
                "Check header level cannot be empty")
        self._level: CheckLevel = check_level

    def get_title(self) -> str:
        return self._title

    def get_status(self) -> Status:
        return self._status

    def get_level(self) -> int:
        return self._level

    def __str__(self) -> str:
        status = self._status.get_str()
        level = str(self._level)
        level_reversed = level[::-1]
        return f"{self._title:<{ConfigValues.CHECK_MAX_HEADER_TITLE_LENGTH}} {level:5}({status}){level_reversed:5}\n"
