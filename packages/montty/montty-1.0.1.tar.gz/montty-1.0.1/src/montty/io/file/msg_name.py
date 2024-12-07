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

from montty.platform.config_values import ConfigValues


# Message files, are how we communicate to the MonTTY manage about check
# report files
#
# The format of message files is:
#     <guid of check report file>.<extension is the message>
#
# There is currently only one message "CLOSE", which is to remove the
# check report file


class MonttyMsgName:
    # Create

    @classmethod
    def create_msg_name_close(cls, guid):
        return cls._create_msg_name(guid, f"{ConfigValues.CHECK_REPORT_CLOSE_MESSAGE}")

    @classmethod
    def _create_msg_name(cls, guid, extension):
        return guid + "." + extension

    # Extract

    @classmethod
    def extract_guid(cls, msg_name):
        msg_name_from_path = msg_name.split('/')[-1]
        guid = msg_name_from_path.split('.')[0]
        return guid

    @classmethod
    def extract_extension(cls, msg_name):
        msg_name_from_path = msg_name.split('/')[-1]
        extension = msg_name_from_path.split('.')[1]
        return extension
