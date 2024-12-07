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
#     BASH_SCRIPTS/mty_util/mtyhost.sh
#     BASH_SCRIPTS/mty_util/mtyservice.sh
#
# Description:
#
#     Check that the SystemD service - 'dnf-automatic-install.timer' is:
#         - Installed,
#         - Enabled,
#         - Active
#

from montty.app.check.check import Check
from montty.app.check.root_check import RootCheck
from montty.app.check.collect_filter_check import CollectFilterCheck
from montty.app.check.bash_check import BashCheck


class CheckFilterDnfAutomatic(RootCheck, CollectFilterCheck):
    def __init__(self):
        self._header_title = 'chk_008_clf_rhel_dnf_automatic.py - Check FILTER'
        super().__init__(self._header_title, level_index=0)

        self._check_filter = CheckFilter()

        self._check_dnf_automatic = CheckDnfAutomatic()

    # @implement
    def _add_checks(self, checks: list[Check]) -> None:
        checks.append(self._check_filter)
        checks.append(self._check_dnf_automatic)


# --------------------------------------------------------------------
# Filter check
# --------------------------------------------------------------------

class CheckFilter(BashCheck):
    def __init__(self):
        header_title = ' (f) Filter DISTRO in "rhel"'
        bash_script = 'mty_util/mtyhost.sh'
        arg1 = 'distro_in'
        arg2 = 'rhel'
        super().__init__(header_title, bash_script, arg1, arg2, level_index=1)


# --------------------------------------------------------------------
# Unattened upgrades service
# --------------------------------------------------------------------

class CheckDnfAutomatic(BashCheck):
    def __init__(self):
        header_title = ' (f) Check Service - DNF AUTOMATIC'
        bash_script = 'mty_util/mtyservice.sh'
        arg1 = 'installed_enabled_active'
        arg2 = 'dnf-automatic-install.timer'
        super().__init__(header_title, bash_script, arg1, arg2, level_index=1)
