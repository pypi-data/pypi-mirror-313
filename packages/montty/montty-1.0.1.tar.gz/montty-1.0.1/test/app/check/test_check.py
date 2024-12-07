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
from montty.app.check.check import Check
from montty.app.check.check_level import CheckLevel
from montty.app.check.check_header import CheckHeader


class TestCheck():
    def test_lt_and_eq(self):
        # Temporarily disable "C0321: More than one statement on a single line"
        # pylint: disable=C0321
        class ExtendedCheck(Check):
            def __init__(self, header_title):
                status = Status.create_okay()
                self.header = CheckHeader(header_title, status, CheckLevel(0))

            def get_body(self): pass
            def get_header(self): return self.header
            def get_status(self): pass
            def run(self): pass
        check1 = ExtendedCheck("aaa")
        check2 = ExtendedCheck("bbb")
        check3 = ExtendedCheck("aaa")
        assert check1 < check2
        assert check2 > check1
        assert check1 == check3
        assert check1 != check2

    def test_get_output(self):
        # Temporarily disable "C0321: More than one statement on a single line"
        # pylint: disable=C0321
        class ExtendedCheck(Check):
            def __init__(self, header, body):
                self._header = header
                self._body = body

            def get_header(self):
                check_header = CheckHeader(
                    self._header,
                    Status.create_okay(),
                    CheckLevel(0))
                return check_header

            def get_body(self): return self._body
            def run(self): print()
            def get_status(self): pass

        check1 = ExtendedCheck("a header", "a body")
        output = check1.get_output()
        assert output.startswith('a header')
        assert '(OKAY)' in output
        assert output.endswith('\na body\n')
