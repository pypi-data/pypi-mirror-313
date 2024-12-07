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

from montty.report.body import Body


class TestBody():
    def test_body(self):
        body_raw = "TEST Test test\n" +  \
                   "-r--r--r-- 1 noone nogroup 101 Jan 01 01:30 nofile.py\n" + \
                   "-r--r--r-- 2 noone nogroup 102 Jan 01 02:30 nofile.py\n" + \
                   "-r--r--r-- 3 noone nogroup 103 Jan 01 03:30 nofile.py\n" + \
                   "-r--r--r-- 4 noone nogroup 104 Jan 01 04:30 nofile.py\n" + \
                   "-r--r--r-- 5 noone nogroup 105 Jan 01 05:30 nofile.py\n" + \
                   "-r--r--r-- 6 noone nogroup 106 Jan 01 06:30 nofile.py\n" + \
                   "-r--r--r-- 7 noone nogroup 107 Jan 01 07:30 nofile.py\n" + \
                   "-r--r--r-- 8 noone nogroup 108 Jan 01 08:30 nofile.py\n" + \
                   "-r--r--r-- 9 noone nogroup 109 Jan 01 09:30 nofile.py"

        body = Body()
        body.set_from_text(body_raw)
        assert body.get_len() == 10

        body_lines = body.get_body()
        assert len(body_lines) == 10
        assert body_lines[0] == "TEST Test test"
        assert body_lines[1] == "-r--r--r-- 1 noone nogroup 101 Jan 01 01:30 nofile.py"
        assert body_lines[9] == "-r--r--r-- 9 noone nogroup 109 Jan 01 09:30 nofile.py"
