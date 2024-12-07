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

import pytest
from montty.app.check.check_level import CheckLevel


class TestCheckLevel():
    def test_check_level_0(self):
        check_level = CheckLevel(0)
        assert check_level.get_index() == 0
        assert str(check_level) == '     '

    def test_check_level_1(self):
        check_level = CheckLevel(1)
        assert check_level.get_index() == 1
        assert str(check_level) == '    .'

    def test_check_level_2(self):
        check_level = CheckLevel(2)
        assert check_level.get_index() == 2
        assert str(check_level) == '   ..'

    def test_check_level_3(self):
        check_level = CheckLevel(3)
        assert check_level.get_index() == 3
        assert str(check_level) == '  ...'

    def test_check_level_4(self):
        check_level = CheckLevel(4)
        assert check_level.get_index() == 4
        assert str(check_level) == ' ....'

    def test_check_level_5(self):
        check_level = CheckLevel(5)
        assert check_level.get_index() == 5
        assert str(check_level) == '.....'

    def test_check_level_bad(self):
        with pytest.raises(Exception):
            CheckLevel(6)
