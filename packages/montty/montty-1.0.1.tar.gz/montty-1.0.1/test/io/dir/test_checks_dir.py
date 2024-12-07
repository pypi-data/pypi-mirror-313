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

from montty.io.dir.checks_dir import ChecksDir


class TestChecksDir():
    def test_get_path_and_files(self):
        checks_dir = ChecksDir()
        assert checks_dir.get_path().endswith("/CHECKS") is True
        assert checks_dir.exists() is True

        # checks files - just expect some files
        assert checks_dir.get_python_check_files()

        # checks.csv
        assert checks_dir.get_checks_file_path().endswith("/checks.csv")

        # get_check_file_path(self, check_file_name):
        assert checks_dir.get_check_file_path('chk_001_bash_listening_ports_with_ss.py').endswith(
            'chk_001_bash_listening_ports_with_ss.py')
