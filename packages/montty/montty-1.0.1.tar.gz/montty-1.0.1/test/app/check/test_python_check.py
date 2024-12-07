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

from abc import ABC, abstractmethod
from montty.app.status import Status
from montty.app.check.check_body import CheckBody
from montty.app.check.python_check import PythonCheck


class FakePythonCheck(PythonCheck, ABC):
    def __init__(self, level_index=0):
        self._header_title = 'Test python check'
        super().__init__(self._header_title, level_index)
        self._cpu_percent = None

    # @implement
    def _run_class(self) -> None:
        pass

    @abstractmethod
    def _set_class_result(self, status: Status, body: CheckBody) -> Status:
        raise Exception("You must implement this method")  # pragma: no cover


class FakePythonCheckOk(FakePythonCheck):
    # @implement
    def _set_class_result(self, status: Status, body: CheckBody) -> Status:
        status.set_okay()
        body.append_text("Test class result was OKAY")


class FakePythonCheckAlert(FakePythonCheck):
    # @implement
    def _set_class_result(self, status: Status, body: CheckBody) -> Status:
        status.set_alert()
        body.append_text("Test class result was ALERT")


#########
# Tests #
#########


class TestPythonCheck():
    # Ignore warning for accessing internal members
    # pylint: disable=W0212
    def test_ok(self):
        python_check = FakePythonCheckOk(level_index=0)
        python_check.run()

        string = str(python_check.get_header())
        assert string.startswith('Test python check')
        assert '(OKAY)' in string
        assert string.endswith('\n')

        assert str(python_check.get_body()) == 'Test class result was OKAY'
        assert python_check.get_status().is_okay()

        output = python_check.get_output()
        assert output.startswith('Test python check')
        assert '(OKAY)' in output
        assert output.endswith('\nTest class result was OKAY\n')

        assert python_check.get_level().get_index() == 0
        assert str(python_check.get_level()) == '     '

    # Ignore warning for accessing internal members
    # pylint: disable=W0212
    def test_alert(self):
        python_check = FakePythonCheckAlert(level_index=1)
        python_check.run()

        string = str(python_check.get_header())
        assert string.startswith('Test python check')
        assert '.(ALERT).' in string
        assert string.endswith('\n')

        assert str(python_check.get_body()) == 'Test class result was ALERT'
        assert python_check.get_status().is_alert()

        output = python_check.get_output()
        assert output.startswith('Test python check')
        assert '.(ALERT).' in output
        assert output.endswith('\nTest class result was ALERT\n')

        assert python_check.get_level().get_index() == 1
        assert str(python_check.get_level()) == '    .'
