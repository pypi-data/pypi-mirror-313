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
from montty.platform.platform_command import PlatformCommand


class TestPlatformCommand():
    def test_basic(self):
        command = PlatformCommand(
            'mty_util/mtyhost.sh', 'host_not_eq', 'fake_host')
        assert command.get_bash_script() == 'mty_util/mtyhost.sh'
        command.run()
        assert command.get_status() == 0
        assert command.get_output() == '-> Test host_not_eq fake_host'

    #########
    # Error #
    #########

    def test_negative_script_name_empty(self):
        with pytest.raises(ValueError):
            PlatformCommand('', 'host_not_eq', 'fake_host')
        with pytest.raises(ValueError):
            PlatformCommand(' ')
        with pytest.raises(ValueError):
            PlatformCommand('  ')
