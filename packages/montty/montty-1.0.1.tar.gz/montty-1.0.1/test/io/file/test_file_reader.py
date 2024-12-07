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
import pytest
from montty.io.file.file_reader import FileReader
from montty.platform.config_values import ConfigValues


class TestFileReader():
    def _write_empty_fixture_file(self, file_name):
        with open(file_name, 'w', encoding="utf-8") as f:
            # Prevent pylint warning message
            f.close()

    def _write_fixture_file_status_na(self, file_name):
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(f"{ConfigValues.LOGO}\n")
            f.write("Host: test_host\n")
            f.write("IPv4: 192.168.0.42\n")
            f.write("Status: NA\n")
            f.write("At: August 02, 2024  03:57:32\n")
            f.write("\n")
            f.write(
                "line  1 ----- ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ -------\n")
            f.write(
                "line  2 line   line   line   line   line   line   line   line   line   line   line   line -\n")

    def _write_fixture_file_status_okay(self, file_name):
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(f"{ConfigValues.LOGO}\n")
            f.write("Host: test_host\n")
            f.write("IPv4: 192.168.0.42\n")
            f.write("Status: OKAY\n")
            f.write("At: August 02, 2024  03:57:32\n")
            f.write("\n")
            f.write(
                "line  1 ----- ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ -------\n")
            f.write(
                "line  2 line   line   line   line   line   line   line   line   line   line   line   line -\n")

    def _write_fixture_file_status_warn(self, file_name):
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(f"{ConfigValues.LOGO}\n")
            f.write("Host: test_host\n")
            f.write("IPv4: 192.168.0.42\n")
            f.write("Status: WARN\n")
            f.write("At: August 02, 2024  03:57:32\n")
            f.write("\n")
            f.write(
                "line  1 ----- ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ -------\n")
            f.write(
                "line  2 line   line   line   line   line   line   line   line   line   line   line   line -\n")

    def _write_fixture_file_status_alert(self, file_name):
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(f"{ConfigValues.LOGO}\n")
            f.write("Host: test_host\n")
            f.write("IPv4: 192.168.0.42\n")
            f.write("Status: ALERT\n")
            f.write("At: August 02, 2024  03:57:32\n")
            f.write("\n")
            f.write(
                "line  1 ----- ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ -------\n")
            f.write(
                "line  2 line   line   line   line   line   line   line   line   line   line   line   line -\n")

    def _write_fixture_file_status_bad(self, file_name):
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(f"{ConfigValues.LOGO}\n")
            f.write("Host: test_host\n")
            f.write("IPv4: 192.168.0.42\n")
            f.write("Status: BADD\n")
            f.write("At: August 02, 2024  03:57:32\n")
            f.write("\n")
            f.write(
                "line  1 ----- ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ -------\n")
            f.write(
                "line  2 line   line   line   line   line   line   line   line   line   line   line   line -\n")

    def _write_fixture_file_bad_keyword(self, file_name):
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(f"{ConfigValues.LOGO}\n")
            f.write("Host: test_host\n")
            f.write("IPv4: 192.168.0.42\n")
            f.write("Status: OKAY\n")
            f.write("At: August 02, 2024  03:57:32\n")
            f.write("Bad: VALUE\n")
            f.write("\n")
            f.write(
                "line  1 ----- ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ -------\n")
            f.write(
                "line  2 line   line   line   line   line   line   line   line   line   line   line   line -\n")

    def test_read_empty_file(self):
        file_name = "file_empty.mty"
        self._write_empty_fixture_file(file_name)
        file_reader = FileReader(file_name)
        with pytest.raises(Exception):
            file_reader.read()
        os.remove(file_name)

    def test_read_file_status_na(self):
        file_name = "file_status_na.mty"
        self._write_fixture_file_status_na(file_name)
        file_reader = FileReader(file_name)
        file_reader.read()
        assert file_reader.get_file_name() == file_name
        assert file_reader.get_header() is not None
        assert file_reader.get_body() is not None
        os.remove(file_name)

    def test_read_file_status_okay(self):
        file_name = "file_status_okay.mty"
        self._write_fixture_file_status_okay(file_name)
        file_reader = FileReader(file_name)
        file_reader.read()
        assert file_reader.get_file_name() == file_name
        assert file_reader.get_header() is not None
        assert file_reader.get_body() is not None
        os.remove(file_name)

    def test_read_file_status_warn(self):
        file_name = "file_status_warn.mty"
        self._write_fixture_file_status_warn(file_name)
        file_reader = FileReader(file_name)
        file_reader.read()
        assert file_reader.get_file_name() == file_name
        assert file_reader.get_header() is not None
        assert file_reader.get_body() is not None
        os.remove(file_name)

    def test_read_file_status_alert(self):
        file_name = "file_status_alert.mty"
        self._write_fixture_file_status_alert(file_name)
        file_reader = FileReader(file_name)
        file_reader.read()
        assert file_reader.get_file_name() == file_name
        assert file_reader.get_header() is not None
        assert file_reader.get_body() is not None
        os.remove(file_name)

    def test_read_file_status_bad(self):
        file_name = "file_status_bad.mty"
        self._write_fixture_file_status_bad(file_name)
        file_reader = FileReader(file_name)
        with pytest.raises(Exception):
            file_reader.read()
        os.remove(file_name)

    def test_read_file_bad_keyword(self):
        file_name = "file_bad_keyword.mty"
        self._write_fixture_file_bad_keyword(file_name)
        file_reader = FileReader(file_name)
        with pytest.raises(Exception):
            file_reader.read()
        os.remove(file_name)
