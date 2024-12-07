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
from montty.app.monitor.monitor_app import MonitorApp


class DataMonitorOkayApp():
    @classmethod
    def setup(cls):
        monitor_app = MonitorApp()
        monitor_app.get_reports_dir().clean()
        return monitor_app

    ##########
    # Create #
    ##########

    @classmethod
    def create_okay_file1(cls, monitor_app):
        file_name = "c123561a33cc4893824dc38db27dfa56_OKAY_1722801901.mty"
        full_file_name = monitor_app.get_reports_dir().get_report_dir_path()+file_name
        FileUtil.touch(full_file_name)
        return (file_name, full_file_name)

    @classmethod
    def create_okay_file2(cls, monitor_app):
        file_name = "c2235612345612345612345612345612_OKAY_1722801901.mty"
        full_file_name = monitor_app.get_reports_dir().get_report_dir_path()+file_name
        FileUtil.touch(full_file_name)
        return (file_name, full_file_name)

    @classmethod
    def create_request_delete_okay_file1(cls, monitor_app):
        file_name = "c123561a33cc4893824dc38db27dfa56_OKAY.close"
        full_file_name = monitor_app.get_reports_dir().get_input_dir_path()+file_name
        FileUtil.touch(full_file_name)

    ##########
    # Delete #
    ##########

    @classmethod
    def clean_files(cls, monitor_app):
        monitor_app.get_reports_dir().clean()

    @classmethod
    def clean_okay_file1(cls, monitor_app):
        FileUtil.delete_file(monitor_app.get_reports_dir().get_report_dir_path()
                             + "c123561a33cc4893824dc38db27dfa56_OKAY_1722801901.mty")

    @classmethod
    def clean_okay_file2(cls, monitor_app):
        FileUtil.delete_file(monitor_app.get_reports_dir().get_report_dir_path()
                             + "c2235612345612345612345612345612_OKAY_1722801901.mty")

    @classmethod
    def clean_request_delete_okay_file1(cls, monitor_app):
        FileUtil.delete_file(monitor_app.get_reports_dir().get_input_dir_path()
                             + "c123561a33cc4893824dc38db27dfa56_OKAY.close")
