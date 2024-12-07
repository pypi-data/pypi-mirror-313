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
import psutil
from montty.app.status import Status
from montty.app.check.root_check import RootCheck
from montty.app.check.check_body import CheckBody
from montty.app.check.collect_all_check import CollectAllCheck
from montty.app.check.python_check import PythonCheck


class CheckSystemCollection(RootCheck, CollectAllCheck):
    def __init__(self):
        self._header_title = 'chk_2_base_classes'
        super().__init__(self._header_title, level_index=0)

        self._cpu_check = SystemCpuDataCheck()
        self._mem_check = SystemMemDataCheck()
        self._disk_check = SystemDiskDataCheck()
        self._net_check = SystemNetDataCheck()
        self._boot_check = SystemBootDataCheck()

    # @implement
    def _add_checks(self, checks) -> None:
        checks.append(self._cpu_check)
        checks.append(self._mem_check)
        checks.append(self._disk_check)
        checks.append(self._net_check)
        checks.append(self._boot_check)


# Sub checks


class SystemCpuDataCheck(PythonCheck):
    def __init__(self):
        self._header_title = "SystemCpuDataCheck"
        super().__init__(self._header_title, level_index=1)
        self._cpu_percent = None
        self._cpu_ghz = None
        self._cpu_count = None

    # @implement
    def _run_class(self) -> None:
        self._cpu_percent = psutil.cpu_percent(interval=2, percpu=False)
        cpu_freq = psutil.cpu_freq()
        self._cpu_ghz = cpu_freq[0] / 1000.0
        self._cpu_count = psutil.cpu_count()

    # @implement
    def _set_class_result(self, status: Status, body: CheckBody) -> None:
        if self._cpu_percent > 95:
            status.set_alert()  # pragma: no cover
        elif self._cpu_percent > 90:
            status.set_warn()  # pragma: no cover
        else:
            status.set_okay()
        body.append_text(f"CPU usage : {self._cpu_percent: 5.1f}%\n")
        body.append_text(f"CPU clock : {self._cpu_ghz: 5.1f}GHz\n")
        body.append_text(f"CPU count : {self._cpu_count: 3}\n")


class SystemMemDataCheck(PythonCheck):
    def __init__(self):
        self._header_title = "SystemMemDataCheck"
        super().__init__(self._header_title, level_index=1)
        self._usage_percent = None

    # @implement
    def _run_class(self) -> None:
        self._usage_percent = psutil.virtual_memory()[2]

    # @implement
    def _set_class_result(self, status: Status, body: CheckBody) -> None:
        if self._usage_percent > 95:
            status.set_alert()  # pragma: no cover
        elif self._usage_percent > 90:
            status.set_warn()  # pragma: no cover
        else:
            status.set_okay()
        body.append_text(f"Mem usage : {self._usage_percent: 5.1f}%\n")


class SystemDiskDataCheck(PythonCheck):
    def __init__(self):
        self._header_title = "SystemDiskDataCheck"
        super().__init__(self._header_title, level_index=1)
        self._usage_percent = None

    # @implement
    def _run_class(self) -> None:
        self._usage_percent = psutil.disk_usage('/')[3]

    # @implement
    def _set_class_result(self, status: Status, body: CheckBody) -> None:
        if self._usage_percent > 95:
            status.set_alert()  # pragma: no cover
        elif self._usage_percent > 90:
            status.set_warn()  # pragma: no cover
        else:
            status.set_okay()
        body.append_text(
            f"Disk      :  parttion:/  usage:{self._usage_percent: 5.1f}%\n")


class SystemNetDataCheck(PythonCheck):
    def __init__(self):
        self._header_title = "SystemNetDataCheck"
        super().__init__(self._header_title, level_index=1)
        self._errin = None
        self._errout = None
        self._dropin = None
        self._dropout = None

    # @implement
    def _run_class(self) -> None:
        net_io = psutil.net_io_counters()
        self._errin = net_io[4]
        self._errout = net_io[5]
        self._dropin = net_io[6]
        self._dropout = net_io[7]

    # @implement
    def _set_class_result(self, status: Status, body: CheckBody) -> None:
        if self._errin >= 5 or self._errout >= 5 or self._dropin >= 5 or self._dropout >= 5:
            status.set_alert()  # pragma: no cover
        elif self._errin > 0 or self._errout > 0 or self._dropin > 0 or self._dropout > 0:
            status.set_warn()  # pragma: no cover
        else:
            status.set_okay()
        body.append_text(
            f"Net       :  errin   : {self._errin: 3}\n")
        body.append_text(
            f"             errout  : {self._errout: 3}\n")
        body.append_text(
            f"             dropin  : {self._dropin: 3}\n")
        body.append_text(
            f"             dropout : {self._dropout: 3}\n")


class SystemBootDataCheck(PythonCheck):
    def __init__(self):
        self._header_title = "SystemBootDataCheck"
        super().__init__(self._header_title, level_index=1)
        self._boot_day = None
        self._suffix = None
        self._boot_date_value = None

    # @implement
    def _run_class(self) -> None:
        boot_date_time = psutil.boot_time()
        self._boot_day = datetime.fromtimestamp(boot_date_time).strftime("%-d")
        if self._boot_day == "1":
            self._suffix = "st"  # pragma: no cover
        elif self._boot_day == "2":
            self._suffix = "nd"  # pragma: no cover
        elif self._boot_day == "3":
            self._suffix = "rd"  # pragma: no cover
        elif self._boot_day == "31":
            self._suffix = "st"  # pragma: no cover
        else:
            self._suffix = "th"  # pragma: no cover
        self._boot_date_value = datetime.fromtimestamp(
            boot_date_time).strftime("%B %Y %H:%M:%S")

    # @implement
    def _set_class_result(self, status: Status, body: CheckBody) -> None:
        # No checking done, we are just displaying the values
        status.set_okay()
        body.append_text(
            f"Boot      :  {self._boot_day}{self._suffix} {self._boot_date_value}\n")
