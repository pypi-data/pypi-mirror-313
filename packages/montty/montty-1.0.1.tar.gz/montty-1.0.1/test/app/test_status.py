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


class TestStatus:

    def test_create(self):
        status = Status.create_alert()
        assert status.is_alert()
        assert status.get_str() == Status.ALERT

        status = Status.create_warn()
        assert status.is_warn()
        assert status.get_str() == Status.WARN

        status = Status.create_okay()
        assert status.is_okay()
        assert status.get_str() == Status.OKAY

        status = Status.create_na()
        assert status.is_na()
        assert status.get_str() == Status.NA

    def test_set(self):
        status = Status()

        status.set_alert()
        assert status.is_alert()
        assert status.get_str() == Status.ALERT

        status.set_warn()
        assert status.is_warn()
        assert status.get_str() == Status.WARN

        status.set_okay()
        assert status.is_okay()
        assert status.get_str() == Status.OKAY

        status.set_na()
        assert status.is_na()
        assert status.get_str() == Status.NA

    # Merge

    def test_merge_to_alert(self):
        status_to = Status()
        status_from = Status()

        status_to.set_alert()
        status_from.set_alert()
        status_to.merge(status_from)
        assert status_to.is_alert()

        status_to.set_alert()
        status_from.set_warn()
        status_to.merge(status_from)
        assert status_to.is_alert()

        status_to.set_alert()
        status_from.set_okay()
        status_to.merge(status_from)
        assert status_to.is_alert()

        status_to.set_alert()
        status_from.set_na()
        status_to.merge(status_from)
        assert status_to.is_alert()

    def test_merge_to_warn(self):
        status_to = Status()
        status_from = Status()

        status_to.set_warn()
        status_from.set_alert()
        status_to.merge(status_from)
        assert status_to.is_alert()

        status_to.set_warn()
        status_from.set_warn()
        status_to.merge(status_from)
        assert status_to.is_warn()

        status_to.set_warn()
        status_from.set_okay()
        status_to.merge(status_from)
        assert status_to.is_warn()

        status_to.set_warn()
        status_from.set_na()
        status_to.merge(status_from)
        assert status_to.is_warn()

    def test_merge_to_okay(self):
        status_to = Status()
        status_from = Status()

        status_to.set_okay()
        status_from.set_alert()
        status_to.merge(status_from)
        assert status_to.is_alert()

        status_to.set_okay()
        status_from.set_warn()
        status_to.merge(status_from)
        assert status_to.is_warn()

        status_to.set_okay()
        status_from.set_okay()
        status_to.merge(status_from)
        assert status_to.is_okay()

        status_to.set_okay()
        status_from.set_na()
        status_to.merge(status_from)
        assert status_to.is_okay()

    def test_merge_to_na(self):
        status_to = Status()
        status_from = Status()

        status_to.set_na()
        status_from.set_alert()
        status_to.merge(status_from)
        assert status_to.is_alert()

        status_to.set_na()
        status_from.set_warn()
        status_to.merge(status_from)
        assert status_to.is_warn()

        status_to.set_na()
        status_from.set_okay()
        status_to.merge(status_from)
        assert status_to.is_okay()

        status_to.set_na()
        status_from.set_na()
        status_to.merge(status_from)
        assert status_to.is_na()

    # Exceptions

    def test_exceptions_get_or_is(self):
        status = Status()
        assert status.is_set() is False
        assert status.is_not_set() is True

        with pytest.raises(Exception):
            status.get_str()
        with pytest.raises(Exception):
            status.is_alert()
        with pytest.raises(Exception):
            status.is_warn()
        with pytest.raises(Exception):
            status.is_okay()
        with pytest.raises(Exception):
            status.is_na()

    def test_exceptions_merge(self):
        # Merge when neither is set
        status = Status()
        assert status.is_not_set() is True
        with pytest.raises(Exception):
            status.merge(Status())

        # Merge to not set, from alert
        assert status.is_not_set() is True
        status_from = Status()
        status_from.set_alert()
        with pytest.raises(Exception):
            status.merge(status_from)

        # Merge to alert, from not set
        status.set_alert()
        assert status.is_set() is True
        status_from = Status()
        with pytest.raises(Exception):
            status.merge(status_from)
