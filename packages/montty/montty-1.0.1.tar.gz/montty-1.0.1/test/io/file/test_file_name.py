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

import re
from montty.io.file.file_name import MonttyFileName


class TestMonttyFileName():
    def test_file_name_na(self):
        file_name = MonttyFileName.create_file_name_na()
        assert len(file_name) == 50

        full_file_name = "/some/path/"+file_name

        guid = MonttyFileName.extract_guid(full_file_name)
        guid_is_alpha_numeric = bool(re.match(r'^[0-9a-zA-Z]+$', str(guid)))
        assert guid_is_alpha_numeric is True

        ttl = MonttyFileName.extract_ttl(full_file_name)
        ttl_is_only_digits = bool(re.match(r'^\d+$', str(ttl)))
        assert ttl_is_only_digits is True

        status = MonttyFileName.extract_status(full_file_name)
        assert status == "NA"

    def test_file_name_okay(self):
        file_name = MonttyFileName.create_file_name_okay()
        assert len(file_name) == 52

        full_file_name = "/some/path/"+file_name

        guid = MonttyFileName.extract_guid(full_file_name)
        guid_is_alpha_numeric = bool(re.match(r'^[0-9a-zA-Z]+$', str(guid)))
        assert guid_is_alpha_numeric is True

        ttl = MonttyFileName.extract_ttl(full_file_name)
        ttl_is_only_digits = bool(re.match(r'^\d+$', str(ttl)))
        assert ttl_is_only_digits is True

        status = MonttyFileName.extract_status(full_file_name)
        assert status == "OKAY"

    def test_create_file_name_warn(self):
        file_name = MonttyFileName.create_file_name_warn()
        assert len(file_name) == 52

        full_file_name = "/some/path/"+file_name

        guid = MonttyFileName.extract_guid(full_file_name)
        guid_is_alpha_numeric = bool(re.match(r'^[0-9a-zA-Z]+$', str(guid)))
        assert guid_is_alpha_numeric is True

        ttl = MonttyFileName.extract_ttl(full_file_name)
        ttl_is_only_digits = bool(re.match(r'^\d+$', str(ttl)))
        assert ttl_is_only_digits is True

        status = MonttyFileName.extract_status(full_file_name)
        assert status == "WARN"

    def test_create_file_name_alert(self):
        file_name = MonttyFileName.create_file_name_alert()
        assert len(file_name) == 53

        full_file_name = "/some/path/"+file_name

        guid = MonttyFileName.extract_guid(full_file_name)
        guid_is_alpha_numeric = bool(re.match(r'^[0-9a-zA-Z]+$', str(guid)))
        assert guid_is_alpha_numeric is True

        ttl = MonttyFileName.extract_ttl(full_file_name)
        ttl_is_only_digits = bool(re.match(r'^\d+$', str(ttl)))
        assert ttl_is_only_digits is True

        status = MonttyFileName.extract_status(full_file_name)
        assert status == "ALERT"
