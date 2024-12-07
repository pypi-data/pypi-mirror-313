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
from montty.platform.config_values import ConfigValues
from montty.platform.platform_values import PlatformValues
from montty.platform.platform_datetime import PlatformDateTime

# <guid>_[NA|OKAY|WARN|ALERT}_<ttl>.mty


class MonttyFileName:
    # Create

    @classmethod
    def create_file_name_na(cls):
        return cls._create_file_name(Status.NA)

    @classmethod
    def create_file_name_okay(cls):
        return cls._create_file_name(Status.OKAY)

    @classmethod
    def create_file_name_warn(cls):
        return cls._create_file_name(Status.WARN)

    @classmethod
    def create_file_name_alert(cls):
        return cls._create_file_name(Status.ALERT)

    @classmethod
    def _create_file_name(cls, status):
        guid = PlatformValues.get_guid()
        ttl = str(PlatformDateTime.get_epoch_time_plus_secs(
            ConfigValues.CHECK_REPORT_FILE_TTL_SECS))
        file_name = guid + "_" + status + "_" + ttl + \
            f"{ConfigValues.CHECK_REPORT_FILE_EXTENSION}"
        return file_name

    # Extract

    @classmethod
    def extract_guid(cls, file_name):
        file_name_from_path = file_name.split('/')[-1]
        file_name_ext_removed = file_name_from_path.split('.')[0]
        guid = file_name_ext_removed.split('_', 2)[0]
        return guid

    @classmethod
    def extract_status(cls, file_name):
        file_name_from_path = file_name.split('/')[-1]
        file_name_ext_removed = file_name_from_path.split('.')[0]
        status = file_name_ext_removed.split('_', 2)[1]
        return status

    @classmethod
    def extract_ttl(cls, file_name):
        file_name_from_path = file_name.split('/')[-1]
        file_name_ext_removed = file_name_from_path.split('.')[0]
        ttl_time = int(file_name_ext_removed.split('_', 2)[2])
        return ttl_time
