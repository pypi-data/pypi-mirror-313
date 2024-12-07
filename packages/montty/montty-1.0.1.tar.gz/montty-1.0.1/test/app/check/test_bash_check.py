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
from montty.app.check.bash_check import BashCheck
from montty.platform.config_values import ConfigValues


class TestBashCheck():
    # Ignore warning for accessing internal members
    # pylint: disable=W0212
    def test_0_arguments_ok(self):
        bash_check = BashCheck('Test', 'mty_util/mtyokay.sh')
        assert bash_check._header_title == "Test"
        assert bash_check._command.get_bash_script() == r'mty_util/mtyokay.sh'
        bash_check.run()

        assert str(bash_check.get_body()
                   ) == 'Exit status code is 0, this becomes status OKAY'
        assert bash_check.get_status().is_okay()

        output = bash_check.get_output()
        assert output.startswith('Test')
        assert '(OKAY)' in output
        assert output.endswith('OKAY\n')

    # Ignore warning for accessing internal members
    # pylint: disable=W0212
    def test_0_arguments_warn(self):
        bash_check = BashCheck('Test', 'mty_util/mtywarn.sh')
        assert bash_check._header_title == "Test"
        assert bash_check._command.get_bash_script() == r'mty_util/mtywarn.sh'
        bash_check.run()

        assert str(bash_check.get_body()
                   ) == 'Exit status code is 255, this becomes status WARN'
        assert bash_check.get_status().is_warn()

        output = bash_check.get_output()
        assert output.startswith('Test')
        assert '(WARN)' in output
        assert output.endswith('WARN\n')

    # Ignore warning for accessing internal members
    # pylint: disable=W0212
    def test_0_arguments_alert(self):
        bash_check = BashCheck('Test', 'mty_util/mtyalert.sh')
        assert bash_check._header_title == "Test"
        assert bash_check._command.get_bash_script() == r'mty_util/mtyalert.sh'
        bash_check.run()

        assert str(bash_check.get_body(
        )) == 'Exit status code is > 0 and < 253, this becomes status ALERT'
        assert bash_check.get_status().is_alert()

        output = bash_check.get_output()
        assert output.startswith('Test')
        assert '(ALERT)' in output
        assert output.endswith('ALERT\n')

    # Ignore warning for accessing internal members
    # pylint: disable=W0212
    def test_0_arguments_na(self):
        bash_check = BashCheck('Test', 'mty_util/mtyna.sh')
        assert bash_check._header_title == "Test"
        assert bash_check._command.get_bash_script() == r'mty_util/mtyna.sh'
        bash_check.run()

        assert str(bash_check.get_body()
                   ) == 'Exit status code is 254, this becomes status NA'
        assert bash_check.get_status().is_na()

        output = bash_check.get_output()
        assert output.startswith('Test')
        assert '(NA)' in output
        assert output.endswith('NA\n')

    ###################
    # Multi arguments #
    ###################

    # Ignore warning for accessing internal members
    # pylint: disable=W0212
    def test_1_arguments(self):
        bash_check = BashCheck('Test', 'mty_util/mtydebug.sh', 'echo_call')
        assert bash_check._header_title == "Test"
        assert bash_check._command.get_bash_script() == r'mty_util/mtydebug.sh'
        bash_check.run()

        assert str(bash_check.get_body()
                   ) == 'Arguments received in the function:\n  echo_call'
        assert bash_check.get_status().is_okay()

        output = bash_check.get_output()
        assert output.startswith('Test')
        assert '(OKAY)' in output
        assert output.endswith('echo_call\n')

    # Ignore warning for accessing internal members
    # pylint: disable=W0212
    def test_2_arguments(self):
        bash_check = BashCheck(
            'Test', 'mty_util/mtydebug.sh', 'echo_call', 'abc')
        assert bash_check._header_title == "Test"
        assert bash_check._command.get_bash_script() == r'mty_util/mtydebug.sh'
        bash_check.run()

        assert str(bash_check.get_body()
                   ) == 'Arguments received in the function:\n  echo_call\n  abc'
        assert bash_check.get_status().is_okay()

        output = bash_check.get_output()
        assert output.startswith('Test')
        assert '(OKAY)' in output
        assert output.endswith('abc\n')

    #############
    # Has level #
    #############

    # Ignore warning for accessing internal members
    # pylint: disable=W0212
    def test_bash_check_has_level(self):
        bash_check = BashCheck("Test", r'mty_util/mtyokay.sh', level_index=1)
        assert bash_check._header_title == "Test"
        assert bash_check._command.get_bash_script() == r'mty_util/mtyokay.sh'
        bash_check.run()

        assert str(bash_check.get_body()
                   ) == 'Exit status code is 0, this becomes status OKAY'
        assert bash_check.get_status().is_okay()

        output = bash_check.get_output()
        assert output.startswith('Test')
        assert '.(OKAY).' in output
        assert output.endswith('status OKAY\n')

        assert bash_check.get_level().get_index() == 1
        assert str(bash_check.get_level()) == '    .'

    ##################
    # Error handling #
    ##################

    def test_restricted_chars_in_args(self):
        restricted_values = [
            ';', '&', '|', '`', '$(', '"', "'", " ",
            '\t', '>', '<', '>>', '<<', '~', '$', '!',
        ]
        for restricted_value in restricted_values:
            with pytest.raises(ValueError):
                BashCheck('Test', 'mty_util/mtydebug.sh', 'echo_call',
                          f'arg_begin{restricted_value}arg_end')

    # Ignore warning for accessing internal members
    # pylint: disable=W0212

    def test_check_status_for_bad_value(self):
        bash_check = BashCheck("Test", r'mty_util/mtyokay.sh')

        # command status should be 0..255, here 256
        with pytest.raises(Exception):
            bash_check._check_result(256, None)

        # command status should be 0..255, here -1
        with pytest.raises(Exception):
            bash_check._check_result(-1, None)

        # command status should be 0..255, here None
        with pytest.raises(Exception):
            bash_check._check_result(None, None)

        # command status should be 0..255, here a string
        with pytest.raises(Exception):
            bash_check._check_result("1", None)

    def test_negative_script_name_not_valid_linux_filename(self):
        with pytest.raises(ValueError):
            not_valid_filename = r'$file.sh'
            BashCheck('Test', not_valid_filename)
        with pytest.raises(ValueError):
            not_valid_filename = r'f$le.sh'
            BashCheck('Test', not_valid_filename)
        with pytest.raises(ValueError):
            not_valid_filename = r'file.sh$'
            BashCheck('Test', not_valid_filename)

    def test_negative_script_name_starts_with_slash(self):
        with pytest.raises(ValueError):
            not_valid_filename = r'/file.sh'
            BashCheck('Test', not_valid_filename)

    def test_negative_script_name_over_max_len(self):
        with pytest.raises(ValueError):
            long_bash_script_name = ConfigValues.BASH_SCRIPT_NAME_MAX_LENGTH * 'a'
            long_bash_script_name += 'a'
            BashCheck('Test', long_bash_script_name)

    def test_negative_script_argument_over_max_len(self):
        with pytest.raises(ValueError):
            long_bash_script_argument = ConfigValues.BASH_SCRIPT_ARGUMENT_MAX_LENGTH * 'a'
            long_bash_script_argument += 'a'
            BashCheck('Test', 'testname.sh', long_bash_script_argument)

    def test_negative_script_argument_empty(self):
        with pytest.raises(ValueError):
            BashCheck('Test', 'testname.sh', '')
