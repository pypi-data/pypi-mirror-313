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

class Status:
    ALERT = "ALERT"
    WARN = "WARN"
    OKAY = "OKAY"
    NA = "NA"

    @classmethod
    def create_alert(cls):
        status = Status()
        status.set_alert()
        return status

    @classmethod
    def create_warn(cls):
        status = Status()
        status.set_warn()
        return status

    @classmethod
    def create_okay(cls):
        status = Status()
        status.set_okay()
        return status

    @classmethod
    def create_na(cls):
        status = Status()
        status.set_na()
        return status

    def __init__(self):
        self._value = None

    def get_str(self):
        if self.is_not_set():
            self.panic()
        if self.is_alert():
            return Status.ALERT
        if self.is_warn():
            return Status.WARN
        if self.is_na():
            return Status.NA
        return Status.OKAY

    # Set

    def set_alert(self):
        self._value = Status.ALERT

    def set_warn(self):
        self._value = Status.WARN

    def set_okay(self):
        self._value = Status.OKAY

    def set_na(self):
        self._value = Status.NA

    def is_set(self):
        return self._value is not None

    def is_not_set(self):
        return self._value is None

    def panic(self):
        raise Exception("Value is not set")

    # Check

    def is_alert(self):
        if self.is_not_set():
            self.panic()
        return self._value == Status.ALERT

    def is_warn(self):
        if self.is_not_set():
            self.panic()
        return self._value == Status.WARN

    def is_okay(self):
        if self.is_not_set():
            self.panic()
        return self._value == Status.OKAY

    def is_na(self):
        if self.is_not_set():
            self.panic()
        return self._value == Status.NA

    # Merge

    def merge(self, from_status):
        if self.is_not_set():
            raise Exception("Merge self status not set")
        if from_status.is_not_set():
            raise Exception("Merge from status not set")

        if self.is_alert() or from_status.is_alert():
            self._value = Status.ALERT
        elif self.is_warn() or from_status.is_warn():
            self._value = Status.WARN
        elif self.is_okay() or from_status.is_okay():
            self._value = Status.OKAY
        else:
            # Both are NA
            self._value = Status.NA
