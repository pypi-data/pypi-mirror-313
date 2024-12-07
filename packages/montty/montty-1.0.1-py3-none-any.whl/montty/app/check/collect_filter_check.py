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
from montty.app.check.check import Check
from montty.app.check.collect_base_check import CollectBaseCheck


class CollectFilterCheck(CollectBaseCheck, ABC):
    # @implement
    def _run_checks(self) -> None:
        ''' Run a collection of checks, if the prior check was OKAY 

        Run each check ONLY if the prior check status was OKAY '''
        self._add_checks(self._checks)

        prior_check: Check = None

        for check in self._checks:
            if not prior_check or prior_check.get_status().is_okay():
                check.run()
                self._status.merge(check.get_status())
                self._body.append_header(check.get_header())
                self._body.append_body(check.get_body())
                prior_check = check
            else:
                self._status.set_na()
                break

    @abstractmethod
    def _add_checks(self, checks: list[Check]) -> None:
        raise Exception("You must override this method")
