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
import ipaddress
from montty.platform.platform_values import PlatformValues


class TestPlatformValues():
    def test_get_hostname(self):
        hostname = PlatformValues.get_hostname()
        is_alpha_numeric = bool(re.match(r'^[0-9a-zA-Z_-]+$', hostname))
        assert is_alpha_numeric is True

    def test_get_ip(self):
        ipv4 = PlatformValues.get_ip()
        is_valid_ip = ipaddress.ip_address(ipv4)
        assert bool(is_valid_ip) is True

    def test_get_guid(self):
        guid = PlatformValues.get_guid()
        is_alpha_numeric = bool(re.match(r'^[0-9a-zA-Z]+$', guid))
        assert is_alpha_numeric is True
