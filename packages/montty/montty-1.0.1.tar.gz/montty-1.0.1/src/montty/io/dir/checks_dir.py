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
import glob
from montty.io.dir.install_dir import InstallDir
from montty.platform.config_values import ConfigValues


class ChecksDir:
    def __init__(self):
        self._install_dir = InstallDir.create_instance()
        self._path = f"{self._install_dir.get_path()}/{ConfigValues.CHECKS_DIR_NAME}"

    def get_path(self):
        return self._path

    def exists(self):
        return os.path.exists(self.get_path())

    def get_python_check_files(self):
        return glob.glob(f"{self.get_path()}/{ConfigValues.GLOB_PATTERN_PYTHON_CHECK_FILES}")

    def get_checks_file_path(self):
        return f"{self.get_path()}/checks.csv"

    def get_check_file_path(self, check_file_name):
        return f"{self.get_path()}/{check_file_name}"
