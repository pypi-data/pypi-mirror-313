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


class FileWriter:
    def __init__(self, file_name):
        self._file_name = file_name
        self._header = None
        self._body = None

    def get_file_name(self):
        return self._file_name

    def get_header(self):
        return self._header

    def set_header(self, header):
        self._header = header

    def get_body(self):
        return self._body

    def set_body(self, body):
        self._body = body

    def write(self):
        with open(self._file_name, 'w', encoding=f"{ConfigValues.FILE_ENCODING}") as f:
            f.write(self._header.get_logo() + '\n')
            f.write('Host: ' + self._header.get_subject().get_hostname() + '\n')
            f.write('IPv4: ' + self._header.get_subject().get_ip() + '\n')
            f.write('Status: ' +
                    self._header.get_subject().get_status().get_str() + '\n')
            f.write('At: ' + self._header.get_subject().get_at() + '\n')

            f.write('\n')

            for line in self._body.get_body():
                f.write(line + '\n')
