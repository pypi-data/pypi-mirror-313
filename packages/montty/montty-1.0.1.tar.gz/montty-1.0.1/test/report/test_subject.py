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


class TestSubject():
    def test_hostname(self):
        subject = Subject()
        hostname = "test_hostname"
        subject.set_hostname(hostname)
        assert subject.get_hostname() == hostname

    def test_ip(self):
        subject = Subject()
        ip = "192.0.2.2"
        subject.set_ip(ip)
        assert subject.get_ip() == ip

    def test_status(self):
        subject = Subject()
        subject.set_status_na()
        assert subject.get_status() is not None
        assert subject.is_status_na() is True

        subject.set_status_okay()
        assert subject.get_status() is not None
        assert subject.is_status_okay() is True

        subject.set_status_warn()
        assert subject.get_status() is not None
        assert subject.is_status_warn() is True

        subject.set_status_alert()
        assert subject.get_status() is not None
        assert subject.is_status_alert() is True

    def test_at(self):
        subject = Subject()
        at = "Some Date/Time"
        subject.set_at(at)
        assert subject.get_at() == at
        subject.set_at_now()
        assert subject.get_at() is not None
        assert subject.get_at() != at
