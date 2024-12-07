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
from montty.report.subject import Subject
from montty.report.header import Header
from montty.report.body import Body


class FileReader:
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

    def read(self):
        with open(self.get_file_name(), 'r', encoding=f"{ConfigValues.FILE_ENCODING}") as f:
            # Skip logo
            f.readline()

            # Get header
            subject = Subject()

            while True:
                # Get next line from file
                line = f.readline()

                # Check the file has content, and is not just empty
                if not line:
                    raise Exception("Premature end of file")

                # Skip empty lines
                if line == '\n':
                    break

                # Format is <keyword> : <value>
                line_split = line.split(':', 1)

                keyword = line_split[0]
                value = line_split[1].strip()
                if keyword.upper() == "HOST":
                    subject.set_hostname(value)
                elif keyword.upper() == "IPV4":
                    subject.set_ip(value)
                elif keyword.upper() == "STATUS":
                    if value.upper() == Status.NA:
                        subject.set_status_na()
                    elif value.upper() == Status.OKAY:
                        subject.set_status_okay()
                    elif value.upper() == Status.WARN:
                        subject.set_status_warn()
                    elif value.upper() == Status.ALERT:
                        subject.set_status_alert()
                    else:
                        raise Exception("Status value not recognized")
                elif keyword.upper() == "AT":
                    subject.set_at(value)
                else:
                    raise Exception(
                        f"Keyword not recognized -> {keyword.upper()}")

            self.set_header(Header(subject))

            # Read body
            body_lines = []
            while True:
                line = f.readline()
                if not line:
                    break
                body_lines.append(line)
            body = Body()
            body.set_from_array(body_lines)

            self.set_body(body)
