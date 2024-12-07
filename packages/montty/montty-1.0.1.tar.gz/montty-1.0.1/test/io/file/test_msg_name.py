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
from montty.io.file.msg_name import MonttyMsgName
from montty.platform.platform_values import PlatformValues


class TestMonttyMsgName():
    def test_msg_name_close(self):
        guid = PlatformValues.get_guid()
        msg_name = MonttyMsgName.create_msg_name_close(guid)
        assert len(msg_name) == 38

        full_msg_name = "/some/path/"+msg_name

        guid = MonttyMsgName.extract_guid(full_msg_name)
        guid_is_alpha_numeric = bool(re.match(r'^[0-9a-zA-Z]+$', str(guid)))
        assert guid_is_alpha_numeric is True

        extension = MonttyMsgName.extract_extension(full_msg_name)
        assert extension == "close"
