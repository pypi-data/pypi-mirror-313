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

import textwrap
# Not in Python 3.9, needs 3.11
# from typing import Self
from montty.app.check.check_header import CheckHeader


class CheckBody:
    def __init__(self):
        self._body_text = ''

    def append_text(self, text) -> None:
        self._body_text += text

    # Self not in Python 3.9, needs 3.11
    # def append_body(self, check_body: Self) -> None:
    def append_body(self, check_body) -> None:
        self.append_text(str(check_body))
        self.append_text("\n")

    def append_header(self, check_header: CheckHeader) -> None:
        self.append_text(str(check_header))
        self.append_text("\n")

    def __str__(self) -> str:
        folded_text = self.fold_lines(self._body_text, width=80)
        return folded_text

    def fold_lines(self, input_string, width=60):
        # Split the input string into lines
        lines = input_string.splitlines()

        # Initialize an empty list to store the folded lines
        folded_lines = []

        # Process each line
        for line in lines:
            # Wrap the current line to the specified width
            wrapped_lines = textwrap.wrap(line, width=width)
            # Add the wrapped lines to the result list
            folded_lines.extend(wrapped_lines)

        return "\n".join(folded_lines)
