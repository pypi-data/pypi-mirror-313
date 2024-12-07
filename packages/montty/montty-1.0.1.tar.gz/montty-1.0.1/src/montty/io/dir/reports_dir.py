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
from montty.app.status import Status
from montty.io.dir.install_dir import InstallDir
from montty.io.file.file_util import FileUtil
from montty.platform.config_values import ConfigValues


class ReportsDir:
    def __init__(self):
        self._install_dir = InstallDir.create_instance()
        self._path = f"{self._install_dir.get_path()}/{ConfigValues.REPORTS_DIR_NAME}"
        self._input_dir_path = self._path + \
            f"/{ConfigValues.REPORTS_DIR_INPUT_DIR_NAME}/"
        self._report_dir_path = self._path + \
            f"/{ConfigValues.REPORTS_DIR_REPORT_DIR_NAME}/"
        self._warn_dir_path = self._path + \
            f"/{ConfigValues.REPORTS_DIR_WARN_DIR_NAME}/"
        self._alert_dir_path = self._path + \
            f"/{ConfigValues.REPORTS_DIR_ALERT_DIR_NAME}/"

    # Install

    def get_install_dir_path(self):
        return self._install_dir.get_path()

    # Reports dir

    def get_path(self):
        return self._path  # pragma: no cover

    def exists(self):
        return os.path.exists(self.get_path())  # pragma: no cover

    # _input dir

    def get_input_dir_path(self):
        return self._input_dir_path

    def input_dir_exists(self):
        return os.path.exists(self.get_input_dir_path())

    def get_input_dir_files(self):
        return glob.glob(self.get_input_dir_path() + f"*{ConfigValues.CHECK_REPORT_FILE_EXTENSION}")

    def get_input_dir_closed_na_files(self):
        return glob.glob(self.get_input_dir_path() + f"*_{Status.NA}{ConfigValues.CHECK_CLOSE_MESSAGE_FILE_EXTENSION}")

    def get_input_dir_closed_okay_files(self):
        return glob.glob(self.get_input_dir_path() + f"*_{Status.OKAY}{ConfigValues.CHECK_CLOSE_MESSAGE_FILE_EXTENSION}")

    def get_input_dir_closed_warn_files(self):
        return glob.glob(self.get_input_dir_path() + f"*_{Status.WARN}{ConfigValues.CHECK_CLOSE_MESSAGE_FILE_EXTENSION}")

    def get_input_dir_closed_alert_files(self):
        return glob.glob(self.get_input_dir_path() + f"*_{Status.ALERT}{ConfigValues.CHECK_CLOSE_MESSAGE_FILE_EXTENSION}")

    # Report dir

    def get_report_dir_path(self):
        return self._report_dir_path

    def report_dir_exists(self):
        return os.path.exists(self.get_report_dir_path())

    def get_report_dir_files(self):
        return glob.glob(self.get_report_dir_path() + f"*{ConfigValues.CHECK_REPORT_FILE_EXTENSION}")

    # _warn dir

    def get_warn_dir_path(self):
        return self._warn_dir_path

    def warn_dir_exists(self):
        return os.path.exists(self.get_warn_dir_path())

    def get_warn_dir_files(self):
        return glob.glob(self.get_warn_dir_path() + f"*{ConfigValues.CHECK_REPORT_FILE_EXTENSION}")

    # _alert dir

    def get_alert_dir_path(self):
        return self._alert_dir_path

    def alert_dir_exists(self):
        return os.path.exists(self.get_alert_dir_path())

    def get_alert_dir_files(self):
        return glob.glob(self.get_alert_dir_path() + f"*{ConfigValues.CHECK_REPORT_FILE_EXTENSION}")

    # All dirs

    def all_dirs_exist(self):
        return  \
            self.input_dir_exists() and \
            self.report_dir_exists() and \
            self.warn_dir_exists() and \
            self.alert_dir_exists()

    # For testing
    def clean(self):
        # Clean input dir
        FileUtil.delete_files(self.get_input_dir_files())
        FileUtil.delete_files(self.get_input_dir_closed_na_files())
        FileUtil.delete_files(self.get_input_dir_closed_okay_files())
        FileUtil.delete_files(self.get_input_dir_closed_warn_files())
        FileUtil.delete_files(self.get_input_dir_closed_alert_files())
        # Clean report dir
        FileUtil.delete_files(self.get_report_dir_files())
        # Clean warn
        FileUtil.delete_files(self.get_warn_dir_files())
        # Clean alert
        FileUtil.delete_files(self.get_alert_dir_files())
