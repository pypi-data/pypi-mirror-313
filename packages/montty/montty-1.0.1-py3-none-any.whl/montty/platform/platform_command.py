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
# See:
#     https://docs.python.org/3/library/subprocess.html#subprocess.getstatusoutput
#     https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
#

# Ignore Bandit warning
# To mitigate, I have take steps to restrict and sanitize the input
#
# Issue: [B404:blacklist] Consider possible security implications associated with the subprocess module.
#   Severity: Low   Confidence: High
#   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
#   More Info: https://bandit.readthedocs.io/en/latest/blacklists/blacklist_imports.html#b404-import-subprocess

import subprocess  # nosec
from montty.io.dir.bash_scripts_dir import BashScriptsDir
from montty.platform.config_values import ConfigValues


class BashRestrictedCharValidator:
    ''' Restrict certain characters from the bash shell script name or arguments

        Semicolon (;):
            Allows command chaining, which can lead to command injection

        Ampersand (&):
            Can run commands in the background or create subshells

        Pipe (|):
            Allows for output redirection between commands

        Backticks (`) and $(...):
            Used for command substitution, which can execute unintended
            commands

        Double quotes (") and single quotes ('):
            Can alter how arguments are interpreted

        Whitespace:
            Depending on context, whitespace can lead to arguments being
            misinterpreted or split unexpectedly

        Redirection operators (>, <, >>, <<):
            Can redirect output or input in unexpected ways

        Tilde (~): 
            Can expand to a user's home directory, potentially exposing
            sensitive information

        Dollar sign ($):
            Used for variable expansion, which could lead to unintended
            variable values being executed

        Exclamation mark (!):
            Can be used in history expansion in some shells
     '''
    restricted_values = [
        ';',
        '&',
        '|',
        '`',
        '$(',
        '"',
        "'",
        " ",
        '\t',
        '>',
        '<',
        '>>',
        '<<',
        '~',
        '$',
        '!',
    ]

    @classmethod
    def check_restricted_chars(cls, bash_script_value: str) -> None:
        for restricted_value in cls.restricted_values:
            if restricted_value in bash_script_value:
                raise ValueError(
                    f'Restricted character value(s) -> "{restricted_value}" found for bash script usage -> {bash_script_value}')


class BashScriptValidator:
    '''Validate bash script name and any arguments, as they originate in user supplied values'''
    @classmethod
    def validate_name(cls, bash_script_name: str, max_length: int) -> None:
        if len(bash_script_name) == 0:
            raise ValueError(
                "Bash script name length, must be > 0")
        if len(bash_script_name) > max_length:
            raise ValueError(
                f"Bash script name length, must be <= max length of {max_length} - {bash_script_name:20}...")
        if bash_script_name.startswith('/'):
            raise ValueError(
                f"Bash script name must not start with '/' - {bash_script_name:20}...")

        BashRestrictedCharValidator.check_restricted_chars(bash_script_name)

    @classmethod
    def validate_argument(cls, bash_script_argument: str, max_length: int) -> None:
        if len(bash_script_argument) == 0:
            raise ValueError(
                "Bash script argument length, must be > 0")
        if len(bash_script_argument) > max_length:
            raise ValueError(
                f"Bash script argument length, must be <= max length of {max_length} - {bash_script_argument:20}...")
        BashRestrictedCharValidator.check_restricted_chars(
            bash_script_argument)


class PlatformCommand:
    def __init__(self, bash_script_name: str, *bash_script_arguments: str):
        self._bash_script_name = bash_script_name.strip()
        BashScriptValidator.validate_name(
            self._bash_script_name, ConfigValues.BASH_SCRIPT_NAME_MAX_LENGTH)

        self._arguments = []
        for argument in bash_script_arguments:
            self._arguments.append(argument.strip())
            BashScriptValidator.validate_argument(
                argument, ConfigValues.BASH_SCRIPT_ARGUMENT_MAX_LENGTH)

        self._status = None
        self._output = None

    def get_bash_script(self) -> str:
        return self._bash_script_name

    def run(self) -> None:
        # pylint: disable=W0201
        # Only run scripts from the scripts dir
        bash_scripts_dir = BashScriptsDir()

        # Construct full command
        bash_script_with_path = bash_scripts_dir.get_full_path(
            self._bash_script_name)
        bash_script_list = ['bash', bash_script_with_path]

        # Add arguments
        for argument in self._arguments:
            bash_script_list.append(argument.strip())

        # Ignore Bandit warning
        # To mitigate, we now add full path to bash_Scripts - so they can only
        # be run from the <project dir> CHECKS/BASH_SCRIPTS directory
        #
        # Issue: [B603:subprocess_without_shell_equals_true] subprocess call - check for execution of untrusted input.
        #   Severity: Low   Confidence: High
        #   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
        #   More Info: https://bandit.readthedocs.io/en/latest/plugins/b603_subprocess_without_shell_equals_true.html
        result = subprocess.run(
            bash_script_list, capture_output=True, text=True, check=False)  # nosec
        self._output = result.stdout.strip()
        self._output += result.stderr.strip()
        self._status = result.returncode

    def get_output(self) -> str:
        return self._output

    def get_status(self) -> int:
        return self._status
