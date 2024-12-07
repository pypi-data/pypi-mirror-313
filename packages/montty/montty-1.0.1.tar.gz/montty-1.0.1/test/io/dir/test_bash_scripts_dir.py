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

import os
from montty.io.dir.bash_scripts_dir import BashScriptsDir


class TestBashScriptsDir():
    def test_bash_scripts_dir(self):
        bash_scripts_dir = BashScriptsDir()
        path = bash_scripts_dir.get_path()
        assert path.endswith("/BASH_SCRIPTS") is True

        assert bash_scripts_dir.exists()
        assert os.path.exists(path)

        fake_script_name = 'some_fake_script.sh'
        script_full_path = bash_scripts_dir.get_full_path(fake_script_name)
        assert script_full_path.endswith(fake_script_name)
        assert path in (script_full_path)
