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

from montty.io.file.file_name import MonttyFileName
from montty.app.status import Status
from . data_monitor_na_app import DataMonitorNaApp


class TestMonitorAppDelete():
    def test_single_file(self):
        monitor_app = DataMonitorNaApp.setup()

        # Have one file, but it is requested to be deleted
        (_, full_na_file_name) = DataMonitorNaApp.create_na_file1(monitor_app)
        DataMonitorNaApp.create_request_delete_na_file1(monitor_app)
        # pylint: disable=W0212
        monitor_app._available_files.append(full_na_file_name)
        assert monitor_app.get_available_files_count() == 1

        guid = MonttyFileName.extract_guid(full_na_file_name)
        # RO801 - Similar lines in 2 files
        # pylint: disable=R0801
        monitor_app.add_request_delete_file(guid, Status.NA)
        assert monitor_app.get_request_delete_files_count() == 1

        # No file, as file was requested to be deleted
        monitor_app.update_next_file()
        assert monitor_app.get_available_files_count() == 0
        assert monitor_app.has_next_file() is False
        assert monitor_app.get_next_file() is None

        # Now delete the request to delete, the file should now come back
        DataMonitorNaApp.clean_request_delete_na_file1(monitor_app)
        monitor_app.update_next_file()
        assert monitor_app.get_request_delete_files_count() == 0
        assert monitor_app.get_available_files_count() == 0
        assert monitor_app.has_next_file() is True
        assert monitor_app.get_next_file() == f"{full_na_file_name}"

        DataMonitorNaApp.clean_files(monitor_app)

    def test_deleted_initial_state(self):
        monitor_app = DataMonitorNaApp.setup()

        assert monitor_app.get_available_files_count() == 0
        assert monitor_app.has_next_file() is False
        assert monitor_app.get_next_file() is None
        assert monitor_app.get_request_delete_files_count() == 0

        monitor_app.add_request_delete_file("123456", Status.NA)
        assert monitor_app.get_request_delete_files_count() == 1

        DataMonitorNaApp.clean_files(monitor_app)
