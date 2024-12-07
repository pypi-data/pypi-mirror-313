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

from montty.platform.config_values import ConfigValues


class CheckLevel():
    def __init__(self, level_index: int):
        if level_index < ConfigValues.CHECK_MIN_LEVEL or level_index > ConfigValues.CHECK_MAX_LEVEL:
            raise Exception(
                f"Check level_index must be in range {ConfigValues.CHECK_MIN_LEVEL}..{ConfigValues.CHECK_MAX_LEVEL}, given {level_index}")
        self._index = level_index

    def get_index(self) -> int:
        return self._index

    def __str__(self) -> str:
        as_string = ''
        for _ in range(self._index):
            as_string += '.'
        return f"{as_string:>{ConfigValues.CHECK_MAX_LEVEL}}"
