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
from montty.report.body import Body
from montty.io.file.file_writer import FileWriter


class TestFileWriter():
    def test_write_file(self, fixture_test_header_status_okay, fixture_body_text_25):
        file_name = "file.mty"
        file_writer = FileWriter(file_name)
        assert file_writer.get_file_name() == file_name

        file_writer.set_header(fixture_test_header_status_okay)
        assert file_writer.get_header() is not None

        body = Body()
        body.set_from_text(fixture_body_text_25)
        file_writer.set_body(body)
        assert file_writer.get_body() is not None

        file_writer.write()

        # Clean up
        os.remove(file_name)
