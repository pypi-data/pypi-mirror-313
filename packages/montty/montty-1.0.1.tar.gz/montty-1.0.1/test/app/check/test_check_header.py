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
from montty.app.status import Status
from montty.app.check.check_level import CheckLevel
from montty.app.check.check_header import CheckHeader


class TestCheckHeader():
    def test_check_header_level_0(self):
        title = "Check title 0"
        status = Status.create_okay()
        check_level = CheckLevel(0)
        check_header = CheckHeader(title, status, check_level)

        string = str(check_header)
        assert string.startswith('Check title 0')
        assert '(OKAY)' in string
        assert string.endswith('\n')

        assert check_header.get_title() == title
        assert check_header.get_status().is_okay()
        assert check_header.get_level().get_index() == 0

    def test_check_header_level_1(self):
        title = "Check title 1"
        status = Status.create_alert()
        check_level = CheckLevel(1)
        check_header = CheckHeader(title, status, check_level)

        string = str(check_header)
        assert string.startswith('Check title 1')
        assert '(ALERT)' in string
        assert string.endswith('\n')

    def test_check_header_level_5(self):
        title = "Check title 5"
        status = Status.create_na()
        check_level = CheckLevel(5)
        check_header = CheckHeader(title, status, check_level)

        string = str(check_header)
        assert string.startswith('Check title 5')
        assert '.....(NA).....' in string
        assert string.endswith('\n')

    def test_check_header_bad_title_len(self):
        title = '123456789_123456789_123456789_123456789_123456789_123456789_123456789_'
        status = Status.create_okay()
        check_level = CheckLevel(2)

        # Should have truncated the header title
        check_header = CheckHeader(title, status, check_level)
        assert check_header.get_title(
        ) == '123456789_123456789_123456789_123456789_123456789_123456789_123**'

    def test_check_header_bad_title_empty(self):
        title1 = None
        title2 = ''
        title3 = ""
        status = Status.create_okay()
        check_level = CheckLevel(3)
        with pytest.raises(Exception):
            CheckHeader(title1, status, check_level)
        with pytest.raises(Exception):
            CheckHeader(title2, status, check_level)
        with pytest.raises(Exception):
            CheckHeader(title3, status, check_level)

    def test_check_header_bad_status_empty(self):
        title = 'Check title'
        status = None
        check_level = CheckLevel(3)
        with pytest.raises(Exception):
            CheckHeader(title, status, check_level)

    def test_check_header_bad_check_level_empty(self):
        title = 'Check title'
        status = Status.create_okay()
        check_level = None
        with pytest.raises(Exception):
            CheckHeader(title, status, check_level)
