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
from montty.app.status import Status
from montty.io.file.file_name import MonttyFileName
from montty.io.file.file_util import FileUtil
from montty.io.dir.reports_dir import ReportsDir
from montty.platform.config_values import ConfigValues
from montty.platform.platform_datetime import PlatformDateTime


class ManagerApp:
    def __init__(self):
        self._reports_dir = ReportsDir()

    def accept_new_reports(self):
        input_files = self._reports_dir.get_input_dir_files()

        for input_file in input_files:
            status = MonttyFileName.extract_status(input_file)

            if status == Status.ALERT:
                report_file = input_file.replace(
                    self._reports_dir.get_input_dir_path(), self._reports_dir.get_alert_dir_path())
            elif status == Status.WARN:
                report_file = input_file.replace(
                    self._reports_dir.get_input_dir_path(), self._reports_dir.get_warn_dir_path())
            else:
                report_file = input_file.replace(
                    self._reports_dir.get_input_dir_path(), self._reports_dir.get_report_dir_path())

            os.replace(input_file, report_file)

    def remove_expired_warn_reports(self):
        """ Remove report files (warn) that have expired - that
            is their TTL is now in the past """
        report_files = self._reports_dir.get_warn_dir_files()
        for report_file in report_files:
            ttl_time = MonttyFileName.extract_ttl(report_file)
            if ttl_time < PlatformDateTime().get_epoch_time():
                os.remove(report_file)

    def remove_expired_okay_and_na_reports(self):
        """ Remove report files (okay and na) that have expired - that
            is their TTL is now in the past """
        report_files = self._reports_dir.get_report_dir_files()
        for report_file in report_files:
            ttl_time = MonttyFileName.extract_ttl(report_file)
            if ttl_time < PlatformDateTime().get_epoch_time():
                os.remove(report_file)

    def remove_nas_requested_delete(self):
        closed_na_files = self._reports_dir.get_input_dir_closed_na_files()

        for closed_na_file in closed_na_files:
            minus_extension = closed_na_file.split(".")
            path_split_up = minus_extension[0].split('/')
            file_name = path_split_up[-1]

            full_file_name = self._reports_dir.get_report_dir_path() + \
                file_name + f"*{ConfigValues.CHECK_REPORT_FILE_EXTENSION}"
            FileUtil.delete_files_by_regex(full_file_name)
            FileUtil.delete_file(closed_na_file)
            # Check warn file was in fact deleted
            if FileUtil.exists(closed_na_file):
                raise Exception(
                    f"Warn msg file was not deleted {closed_na_file}")  # pragma: no cover

    def remove_okays_requested_delete(self):
        closed_okay_files = self._reports_dir.get_input_dir_closed_okay_files()

        for closed_okay_file in closed_okay_files:
            minus_extension = closed_okay_file.split(".")
            path_split_up = minus_extension[0].split('/')
            file_name = path_split_up[-1]

            full_file_name = self._reports_dir.get_report_dir_path() + \
                file_name + f"*{ConfigValues.CHECK_REPORT_FILE_EXTENSION}"
            FileUtil.delete_files_by_regex(full_file_name)
            FileUtil.delete_file(closed_okay_file)
            # Check warn file was in fact deleted
            if FileUtil.exists(closed_okay_file):
                raise Exception(
                    f"Warn msg file was not deleted {closed_okay_file}")  # pragma: no cover

    def remove_warns_requested_delete(self):
        closed_warn_files = self._reports_dir.get_input_dir_closed_warn_files()

        for closed_warn_file in closed_warn_files:
            minus_extension = closed_warn_file.split(".")
            path_split_up = minus_extension[0].split('/')
            file_name = path_split_up[-1]

            full_file_name = self._reports_dir.get_warn_dir_path() + \
                file_name + f"*{ConfigValues.CHECK_REPORT_FILE_EXTENSION}"
            FileUtil.delete_files_by_regex(full_file_name)
            FileUtil.delete_file(closed_warn_file)
            # Check warn file was in fact deleted
            if FileUtil.exists(closed_warn_file):
                raise Exception(
                    f"Warn msg file was not deleted {closed_warn_file}")  # pragma: no cover

    def remove_alerts_requested_delete(self):
        closed_alert_files = self._reports_dir.get_input_dir_closed_alert_files()

        for closed_alert_file in closed_alert_files:
            minus_extension = closed_alert_file.split(".")
            path_split_up = minus_extension[0].split('/')
            file_name = path_split_up[-1]
            # Remove the _ALERT so we have just the guid
            file_name = file_name.replace(f"_{Status.ALERT}", "")

            full_file_name = self._reports_dir.get_alert_dir_path() + \
                file_name + f"*{ConfigValues.CHECK_REPORT_FILE_EXTENSION}"
            FileUtil.delete_files_by_regex(full_file_name)

            FileUtil.delete_file(closed_alert_file)
            # Check alert file was in fact deleted
            if FileUtil.exists(closed_alert_file):
                raise Exception(
                    f"Alert msg file was not deleted {closed_alert_file}")  # pragma: no cover
