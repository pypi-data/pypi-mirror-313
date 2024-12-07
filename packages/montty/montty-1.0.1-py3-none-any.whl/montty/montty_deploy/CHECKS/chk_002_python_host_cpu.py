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

#
# Dependencies:
#
#     CHECKS/PYTHON_LIBS/system_data.py
#
# Description:
#
#     Check system cpu data using python based check
#

from system_data import SystemCpuDataCheck
from montty.app.check.check_body import CheckBody
from montty.app.check.python_check import PythonCheck
from montty.app.check.root_check import RootCheck
from montty.app.status import Status


class CheckHostCpu(RootCheck, PythonCheck):
    def __init__(self):
        header_title = 'chk_002_python_host_cpu.py - HOST CPU'
        super().__init__(header_title)
        self.cpu_check = SystemCpuDataCheck()

    # @implement
    def _run_class(self) -> None:
        self.cpu_check._run_class()

    # @implement
    def _set_class_result(self, status: Status, body: CheckBody) -> None:
        self.cpu_check._set_class_result(status, body)
