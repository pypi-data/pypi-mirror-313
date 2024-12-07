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

import re
from montty.platform.platform_datetime import PlatformDateTime


class TestPlatformDateTime():
    def test_get_now(self):
        now = PlatformDateTime.get_now()
        print("DATE/TIME Now: ", now)

    def test_get_day_month_year(self):
        date_value = PlatformDateTime.get_day_month_year()
        print("DATE Day/Month/Year: ", date_value)

    def test_get_epoch_time(self):
        value = PlatformDateTime().get_epoch_time()
        is_only_digits = bool(re.match(r'^\d+$', str(value)))
        assert is_only_digits is True

    def test_get_epoch_time_plus_secs(self):
        value = PlatformDateTime.get_epoch_time()
        plus_seconds = 60
        value_plus_seconds = PlatformDateTime.get_epoch_time_plus_secs(
            plus_seconds)
        assert (value_plus_seconds - value) == 60
