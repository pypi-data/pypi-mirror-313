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

from montty.app.status import Status
from montty.app.check.root_check import RootCheck
from montty.app.check.check_body import CheckBody
from montty.app.check.collect_all_check import CollectAllCheck
from montty.app.check.python_check import PythonCheck


class SomeOtherFakeClass:
    # Just for test use
    pass


# Root check class, with 3 base classes
class CheckFakeCollection(RootCheck, CollectAllCheck, SomeOtherFakeClass):
    def __init__(self):
        self._header_title = 'chk_3_base_classes'
        super().__init__(self._header_title, level_index=0)

        self._fake_sub_check = FakeSubCheck()

    # @implement
    def _add_checks(self, checks) -> None:
        checks.append(self._fake_sub_check)


class FakeSubCheck(PythonCheck):
    def __init__(self):
        self._header_title = "FakeSubCheck"
        super().__init__(self._header_title, level_index=1)

    # @implement
    def _run_class(self) -> None:
        pass

    # @implement
    def _set_class_result(self, status: Status, body: CheckBody) -> None:
        status.set_okay()
        body.append_text('Fake sub check\n')
