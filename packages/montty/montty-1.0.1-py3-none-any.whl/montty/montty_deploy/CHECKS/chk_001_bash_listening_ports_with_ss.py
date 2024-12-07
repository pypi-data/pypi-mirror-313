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

#
# Dependencies:
#
#     BASH_SCRIPTS/check_listening_ports_with_ss.sh
#
# Description:
#
#     Check listening ports, using Linux "ss" command '''
#

from montty.app.check.root_check import RootCheck
from montty.app.check.bash_check import BashCheck


class CheckListeningPorts(RootCheck, BashCheck):
    ''' Check listening sockets, using Linux "ss" command '''

    def __init__(self):
        header_title = 'chk_001_bash_listening_ports_with_ss.py - LISTENING TCP PORTS'
        bash_script = 'check_listening_ports_with_ss.sh'
        super().__init__(header_title, bash_script)
