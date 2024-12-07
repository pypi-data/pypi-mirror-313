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

from montty.app.status import Status
from montty.io.file.file_util import FileUtil
from montty.io.dir.reports_dir import ReportsDir


class MonitorApp():
    def __init__(self):
        self._reports_dir = ReportsDir()
        self._available_files = []
        self._current_file = None
        self._request_delete_files = []

    # report files

    def get_reports_dir(self):
        return self._reports_dir

    # Next file

    def update_next_file(self):
        # Cached files
        self._current_file = None

        if len(self._available_files) > 0:
            self._current_file = self._available_files.pop()
        else:
            # Clear requests for check file report deletion, as the files are now deleted
            for guid in self._request_delete_files:
                guid_file = self.get_reports_dir().get_input_dir_path() + guid
                if not FileUtil.exists(guid_file + f"_{Status.ALERT}.close") \
                   and \
                   not FileUtil.exists(guid_file + f"_{Status.WARN}.close") \
                   and \
                   not FileUtil.exists(guid_file + f"_{Status.OKAY}.close") \
                   and \
                   not FileUtil.exists(guid_file + f"_{Status.NA}.close"):
                    self._request_delete_files.remove(guid)

            # Load available files

            # Check first for alerts
            self._available_files = self.get_reports_dir().get_alert_dir_files()

            # If no alerts then check for warnings
            if len(self._available_files) == 0:
                self._available_files = self.get_reports_dir().get_warn_dir_files()

            # If no warnings then check for ordinary reports
            if len(self._available_files) == 0:
                self._available_files = self.get_reports_dir().get_report_dir_files()

            # Remove files that have request for delete
            if len(self._available_files) > 0:
                for guid in self._request_delete_files:
                    guid_file = self.get_reports_dir().get_input_dir_path() + guid
                    if FileUtil.exists(guid_file + f"_{Status.ALERT}.close") \
                            or \
                            FileUtil.exists(guid_file + f"_{Status.WARN}.close") \
                            or \
                            FileUtil.exists(guid_file + f"_{Status.OKAY}.close") \
                            or \
                            FileUtil.exists(guid_file + f"_{Status.NA}.close"):
                        for file in self._available_files:
                            if guid in file:
                                self._available_files.remove(file)

            # Get next file (if there are any still available)
            if len(self._available_files) > 0:
                self._current_file = self._available_files.pop()

    def has_next_file(self):
        return self._current_file is not None

    def get_next_file(self):
        return self._current_file

    # Available files

    def get_available_files_count(self):
        return len(self._available_files)

    # Request delete files

    def add_request_delete_file(self, guid, status):
        """ Add a <guid>_ALERT.close msg file 

        guid is the montty file guid value as a string
        status is the the montty file status value as a string (needs to be uppercase)
        """
        self._request_delete_files.append(guid)
        full_msg_file_name = self.get_reports_dir().get_input_dir_path() + \
            guid + "_" + status + ".close"
        FileUtil.touch(full_msg_file_name)
        # Check the file now exists
        does_exist = FileUtil.exists(full_msg_file_name)
        if not does_exist:
            raise Exception(
                f"Close file not created {full_msg_file_name}")  # pragma: no cover
        for available_file in self._available_files:
            if guid in available_file:
                self._available_files.remove(available_file)

    def get_request_delete_files_count(self):
        return len(self._request_delete_files)
