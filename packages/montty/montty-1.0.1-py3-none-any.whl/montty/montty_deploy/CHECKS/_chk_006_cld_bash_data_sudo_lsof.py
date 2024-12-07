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
#         /usr/bin/lsof -i
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#
# Dependencies:
#
#     DATA_FILES/chk_006_lsof.csv
#     BASH_SCRIPTS/mty_util/mtylsof.sh
#
# Description:
#
#     Runs a BaSH script that uses the Linux "lsof" command, to get outgoing
#     port connections
#
#     Details of "allowed" port connections, are read from a CSV "data file"
#
#     The checks are run as a collection "depend" check, that runs each check,
#     ONLY if the # prior check was OKAY
#
#     Checks:
#         - The user has the sudo ability to run the lsof command, so they can see
#               the full output from lsof
#
#         - The output from lsof, comparing against "allowed" connections, from a csv
#               "data file". This file is under the DATA_FILES sub-directory
#

# Self not available in Python 3.9, needs 3.11
#   from typing import Self
from lsof_command_data import AllowedLsofRowValues
from lsof_command_data import ActualLsofRowValues
from montty.app.status import Status
from montty.app.check.check import Check
from montty.app.check.root_check import RootCheck
from montty.app.check.collect_depend_check import CollectDependCheck
from montty.app.check.bash_check import BashCheck
from montty.io.dir.data_files_dir import DataFilesDir


class LsofCollectionDependCheck(RootCheck, CollectDependCheck):
    def __init__(self):
        header_title = 'chk_006_cld_bash_data_sudo_lsof.py - OUTGOING CONNECTIONS (LSOF)'
        super().__init__(header_title, level_index=0)

        # Check we have sudo ability for lsof command
        self._lsof_sudo_ability_check = LsofSudoAbilityCheck()

        # Data file of allowed values
        data_files_dir = DataFilesDir()
        data_file_full_name = data_files_dir.get_full_path('chk_006_lsof.csv')

        # Check lsof command output matches allowed values from data file
        self._lsof_results_check = LsofResultsCheck(data_file_full_name)

    # @implement
    def _add_checks(self, checks: list[Check]) -> None:
        checks.append(self._lsof_sudo_ability_check)
        checks.append(self._lsof_results_check)


class LsofSudoAbilityCheck(BashCheck):
    def __init__(self):
        header_title = ' (d) LsofSudoAbilityCheck - SUDO ABILITY'
        bash_script = 'mty_util/mtylsof.sh'
        arg1 = 'sudo_ability'
        super().__init__(header_title, bash_script, arg1, level_index=1)

    # @override
    def _get_command_output(self, status: Status, command_output: str) -> str:
        if not status.is_okay():
            return command_output
        return ''


class LsofResultsCheck(BashCheck):
    def __init__(self, data_file_full_name: str):
        header_title = ' (d) LsofResultsCheck - PORTS RECOGNIZED'
        bash_script = 'mty_util/mtylsof.sh'
        arg1 = 'ports'
        super().__init__(header_title, bash_script, arg1, level_index=1)

        self._data_file_full_name = data_file_full_name
        self._allowed_lsof_values = None
        self._actual_lsof_values = None

    # @override
    def _check_result(self, _, command_output):
        # Get allowed LSOF values
        self._allowed_lsof_values = AllowedLsofRowValues()
        self._allowed_lsof_values.read_values(self._data_file_full_name)

        # Get actual LSOF values
        self._actual_lsof_values = ActualLsofRowValues(command_output)
        self._actual_lsof_values.parse()

        status = Status()
        if self._allowed_lsof_values.contains_all_values(self._actual_lsof_values):
            status.set_okay()
        else:
            status.set_alert()
        return status

    # @override
    def _get_command_output(self, status: Status, _command_output: str) -> str:
        text = ''
        if not status.is_okay():
            text += "Allowed values:\n"
            text += "--------------\n"
            text += f"{str(self._allowed_lsof_values)}\n"
            text += "Actual values:\n"
            text += "-------------\n"
            text += f"{str(self._actual_lsof_values)}\n"
            text += "Mismatches:\n"
            text += "----------\n"
            text += f"{self._allowed_lsof_values.get_mismatches()}\n"
        return text
