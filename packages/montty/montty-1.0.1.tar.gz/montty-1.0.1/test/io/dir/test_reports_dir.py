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

from montty.io.dir.reports_dir import ReportsDir


class TestReportsDir():
    @classmethod
    def init(cls):
        reports_dir = ReportsDir()
        reports_dir.clean()
        return reports_dir

    def test_install_path(self):
        reports_dir = TestReportsDir.init()
        assert reports_dir.get_install_dir_path().endswith("/montty") is True

    def test_input_dir(self):
        reports_dir = TestReportsDir.init()
        assert reports_dir.get_input_dir_path().endswith("/_input/") is True
        assert reports_dir.input_dir_exists() is True
        # []
        assert not reports_dir.get_input_dir_files()
        # []
        assert not reports_dir.get_input_dir_closed_alert_files()

    def test_report_dir(self):
        reports_dir = TestReportsDir.init()
        assert reports_dir.get_report_dir_path().endswith("/_report/") is True
        assert reports_dir.report_dir_exists() is True
        # []
        assert not reports_dir.get_report_dir_files()

    def test_alert_dir(self):
        reports_dir = TestReportsDir.init()
        assert reports_dir.get_alert_dir_path().endswith("/_alert/") is True
        assert reports_dir.alert_dir_exists() is True
        # []
        assert not reports_dir.get_alert_dir_files()

    def test_all_dirs_exist(self):
        reports_dir = TestReportsDir.init()
        assert reports_dir.all_dirs_exist()
