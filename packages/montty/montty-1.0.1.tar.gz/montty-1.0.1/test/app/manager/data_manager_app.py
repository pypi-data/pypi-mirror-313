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

from montty.io.file.file_util import FileUtil
from montty.io.dir.reports_dir import ReportsDir
from montty.app.manager.manager_app import ManagerApp

# R0904: Too many public methods
# pylint: disable=R0904


class DataManagerApp():
    @classmethod
    def setup(cls):
        cls.clean_files()
        manager_app = ManagerApp()
        return manager_app

    @classmethod
    def clean_files(cls):
        reports_dir = ReportsDir()
        reports_dir.clean()
        return reports_dir

    ############
    # NA file1 #
    ############

    @classmethod
    def na_file1_name(cls):
        return "f1111111111111111111111111111111_NA_1000000000.mty"

    @classmethod
    def create_input_dir_file_na1(cls):
        file_name = cls.na_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_input_dir_path() + file_name
        FileUtil.touch(full_file_name)
        return (file_name, full_file_name)

    @classmethod
    def exists_report_dir_file_na1(cls):
        file_name = cls.na_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_report_dir_path() + file_name
        return FileUtil.exists(full_file_name)

    ##################
    # NA close file1 #
    ##################

    @classmethod
    def close_na_file1_name(cls):
        return "f1111111111111111111111111111111_NA.close"

    @classmethod
    def create_input_dir_close_na_file1(cls):
        file_name = cls.close_na_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_input_dir_path() + file_name
        FileUtil.touch(full_file_name)

    @classmethod
    def exists_input_dir_close_file_na1(cls):
        file_name = cls.close_na_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_input_dir_path() + file_name
        return FileUtil.exists(full_file_name)

    ##############
    # OKAY file1 #
    ##############

    @classmethod
    def okay_file1_name(cls):
        return "f1111111111111111111111111111111_OKAY_1000000000.mty"

    @classmethod
    def create_input_dir_file_okay1(cls):
        file_name = cls.okay_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_input_dir_path() + file_name
        FileUtil.touch(full_file_name)
        return (file_name, full_file_name)

    @classmethod
    def exists_report_dir_file_okay1(cls):
        file_name = cls.okay_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_report_dir_path() + file_name
        return FileUtil.exists(full_file_name)

    ####################
    # OKAY close file1 #
    ####################

    @classmethod
    def close_okay_file1_name(cls):
        return "f1111111111111111111111111111111_OKAY.close"

    @classmethod
    def create_input_dir_close_okay_file1(cls):
        file_name = cls.close_okay_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_input_dir_path() + file_name
        FileUtil.touch(full_file_name)

    @classmethod
    def exists_input_dir_close_file_okay1(cls):
        file_name = cls.close_okay_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_input_dir_path() + file_name
        return FileUtil.exists(full_file_name)

    ##############
    # WARN file1 #
    ##############

    @classmethod
    def warn_file1_name(cls):
        return "f1111111111111111111111111111111_WARN_1000000000.mty"

    @classmethod
    def create_input_dir_file_warn1(cls):
        file_name = cls.warn_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_input_dir_path() + file_name
        FileUtil.touch(full_file_name)
        return (file_name, full_file_name)

    @classmethod
    def exists_warn_dir_file_warn1(cls):
        file_name = cls.warn_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_warn_dir_path() + file_name
        return FileUtil.exists(full_file_name)

    ####################
    # WARN close file1 #
    ####################

    @classmethod
    def close_warn_file1_name(cls):
        return "f1111111111111111111111111111111_WARN.close"

    @classmethod
    def create_input_dir_close_warn_file1(cls):
        file_name = cls.close_warn_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_input_dir_path() + file_name
        FileUtil.touch(full_file_name)

    @classmethod
    def exists_input_dir_close_file_warn1(cls):
        file_name = cls.close_warn_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_input_dir_path() + file_name
        return FileUtil.exists(full_file_name)

    ###############
    # ALERT file1 #
    ###############

    @classmethod
    def alert_file1_name(cls):
        return "f1111111111111111111111111111111_ALERT_1000000000.mty"

    @classmethod
    def create_input_dir_file_alert1(cls):
        file_name = cls.alert_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_input_dir_path() + file_name
        FileUtil.touch(full_file_name)
        return (file_name, full_file_name)

    @classmethod
    def exists_alert_dir_file_alert1(cls):
        file_name = cls.alert_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_alert_dir_path() + file_name
        return FileUtil.exists(full_file_name)

    #####################
    # ALERT close file1 #
    #####################

    @classmethod
    def close_alert_file1_name(cls):
        return "f1111111111111111111111111111111_ALERT.close"

    @classmethod
    def create_input_dir_close_alert_file1(cls):
        file_name = cls.close_alert_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_input_dir_path() + file_name
        FileUtil.touch(full_file_name)

    @classmethod
    def exists_input_dir_close_file_alert1(cls):
        file_name = cls.close_alert_file1_name()
        reports_dir = ReportsDir()
        full_file_name = reports_dir.get_input_dir_path() + file_name
        return FileUtil.exists(full_file_name)
