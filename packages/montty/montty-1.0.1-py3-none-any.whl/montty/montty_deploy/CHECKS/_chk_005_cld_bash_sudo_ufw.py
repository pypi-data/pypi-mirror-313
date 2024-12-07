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

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# Note:
#
#     Requires the user to be able to run the following sudo command:
#
#         /usr/sbin/ufw status verbose
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#
# Dependencies:
#
#     BASH_SCRIPTS/mty_util/mtyufw.sh
#
# Description:
#
#     Runs BaSH scripts to check:
#         - Uncomplicated FireWall (UFW) is installed
#         - The user has the ability to run the required sudo command, to get
#               the current UFW rules
#         - Runs the sudo command, to get the UFW rules, and check they are
#               as expected
#

from montty.app.status import Status
from montty.app.check.check import Check
from montty.app.check.root_check import RootCheck
from montty.app.check.collect_depend_check import CollectDependCheck
from montty.app.check.bash_check import BashCheck


class CheckUncomplicatedFireWall(RootCheck, CollectDependCheck):
    def __init__(self):
        header_title = 'chk_005_cld_bash_sudo_ufw.py - UNCOMPLICATED FIREWALL (UFW)'
        super().__init__(header_title, level_index=0)

        # Is UFW installed
        self._ufw_installed = UfwInstalled()

        # Do I have sudo access to its command so I can check its full status to
        # see the rules configured
        self._ufw_sudo_ability = UfwSudoAbility()

        # Check the full status and see if the expected rules have been configured
        self._ufw_rules = UfwRules()

    # @implement
    def _add_checks(self, checks: list[Check]) -> None:
        checks.append(self._ufw_installed)
        checks.append(self._ufw_sudo_ability)
        checks.append(self._ufw_rules)


# --------------------------------------------------------------------
# Check Uncomplicated Firewall (UFW)
# --------------------------------------------------------------------


class UfwInstalled(BashCheck):
    def __init__(self):
        super().__init__(' (d) UFW INSTALLED', 'mty_util/mtyufw.sh', 'installed', level_index=1)

    # @override
    def _get_command_output(self, status: Status, command_output: str) -> str:
        # Only return the command's output if the status is not OKAY, just
        # to keep the check display simpler with less "noise"
        if not status.is_okay():
            return command_output
        return ''


class UfwSudoAbility(BashCheck):
    def __init__(self):
        super().__init__(' (d) UFW SUDO ABILITY',
                         'mty_util/mtyufw.sh', 'sudo_ability', level_index=1)

    # @override
    def _get_command_output(self, status: Status, command_output: str) -> str:
        # Only return the command's output if the status is not OKAY, just
        # to keep the check display simpler with less "noise"
        if not status.is_okay():
            return command_output
        return ''


class UfwRules(BashCheck):
    def __init__(self):
        super().__init__(' (d) UFW RULES', 'mty_util/mtyufw.sh', 'rules', level_index=1)

    # @override
    def _get_command_output(self, status: Status, command_output: str) -> str:
        # Only return the command's output if the status is not OKAY, just
        # to keep the check display simpler with less "noise"
        if not status.is_okay():
            return command_output
        return ''

    # @override
    def _check_result(self, _: int, command_output: str) -> Status:
        # We need a check that does more that just checks the output status
        # code of the command. Here we looked for expected text in the
        # command's output, for the determination of the check's status
        self._status = Status()
        output_lines = command_output.splitlines()
        if output_lines[0] == 'Status: active' and \
                output_lines[1] == 'Logging: on (low)' and \
                output_lines[2] == 'Default: deny (incoming), allow (outgoing), disabled (routed)' and \
                output_lines[3] == 'New profiles: skip':
            self._status.set_okay()
        else:
            self._status.set_alert()
        return self._status
