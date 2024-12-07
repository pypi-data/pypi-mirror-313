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

from datetime import datetime
from montty.app.status import Status


class Subject:
    def __init__(self):
        self._hostname = ""
        self._ip = ""
        self._status = None
        self._at = ""

    def get_hostname(self):
        return self._hostname

    def set_hostname(self, hostname: str):
        self._hostname = hostname

    def get_ip(self):
        return self._ip

    def set_ip(self, ip: str):
        self._ip = ip

    # Status

    def get_status(self):
        return self._status

    def set_status_na(self):
        self._status = Status()
        self._status.set_na()

    def is_status_na(self):
        return self._status.is_na()

    def set_status_okay(self):
        self._status = Status()
        self._status.set_okay()

    def is_status_okay(self):
        return self._status.is_okay()

    def set_status_warn(self):
        self._status = Status()
        self._status.set_warn()

    def is_status_warn(self):
        return self._status.is_warn()

    def set_status_alert(self):
        self._status = Status()
        self._status.set_alert()

    def is_status_alert(self):
        return self._status.is_alert()

    def get_at(self):
        return self._at

    def set_at_now(self):
        # pylint: disable=C0209
        self._at = "{:%B %d, %Y %H:%M:%S}".format(datetime.now())

    def set_at(self, at: datetime):
        self._at = at
