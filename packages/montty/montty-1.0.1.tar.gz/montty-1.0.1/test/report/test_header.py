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

from montty.report.subject import Subject
from montty.report.header import Header
from montty.platform.config_values import ConfigValues


class TestHeader():
    def test_subject(self):
        subject = Subject()
        hostname = "test_hostname"
        subject.set_hostname(hostname)
        ip = "192.168.0.42"
        subject.set_ip(ip)
        subject.set_status_okay()
        at = "Some Date/Time"
        subject.set_at(at)

        header = Header(subject)

        assert header.get_subject().get_hostname() == hostname
        assert header.get_subject().get_ip() == ip
        assert header.get_subject().get_status().is_okay() is True
        assert header.get_subject().get_at() == at

    def test_logo(self):
        header = Header(Subject())
        assert header.get_logo() == ConfigValues.LOGO
