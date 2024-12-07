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

from . data_monitor_warn_app import DataMonitorWarnApp

# Ignore duplicate code warning
# pylint: disable=R0801


class TestMonitorAppDouble():
    def test_two_files(self):
        monitor_app = DataMonitorWarnApp.setup()

        (_, full_file_name_1) = DataMonitorWarnApp.create_warn_file1(monitor_app)
        (_, full_file_name_2) = DataMonitorWarnApp.create_warn_file2(monitor_app)

        # Initial
        monitor_app.update_next_file()
        assert monitor_app.get_available_files_count() == 1
        assert monitor_app.has_next_file() is True
        assert monitor_app.get_next_file() == f"{full_file_name_2}"
        #
        monitor_app.update_next_file()
        assert monitor_app.get_available_files_count() == 0
        assert monitor_app.has_next_file() is True
        assert monitor_app.get_next_file() == f"{full_file_name_1}"

        # Reload cache
        monitor_app.update_next_file()
        assert monitor_app.get_available_files_count() == 1
        assert monitor_app.has_next_file() is True
        assert monitor_app.get_next_file() == f"{full_file_name_2}"
        #
        monitor_app.update_next_file()
        assert monitor_app.get_available_files_count() == 0
        assert monitor_app.has_next_file() is True
        assert monitor_app.get_next_file() == f"{full_file_name_1}"

        # Delete file1, now have just 1 file - file2

        DataMonitorWarnApp.clean_warn_file1(monitor_app)

        monitor_app.update_next_file()
        assert monitor_app.get_available_files_count() == 0
        assert monitor_app.has_next_file() is True
        assert monitor_app.get_next_file() == f"{full_file_name_2}"

        # Delete file2, now have 0 files

        DataMonitorWarnApp.clean_warn_file2(monitor_app)

        monitor_app.update_next_file()
        assert monitor_app.get_available_files_count() == 0
        assert monitor_app.has_next_file() is False
        assert monitor_app.get_next_file() is None

        DataMonitorWarnApp.clean_files(monitor_app)
