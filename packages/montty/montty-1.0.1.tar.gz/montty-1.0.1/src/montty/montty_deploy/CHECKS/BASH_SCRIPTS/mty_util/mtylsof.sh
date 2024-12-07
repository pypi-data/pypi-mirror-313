#!/bin/bash

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
# For getting listeining ports using the Linux command "lsof -i":
#     lsof -i
#       lsof: List open files
#         -i: list all network files
#
# Note:
#     The user must be able for sudo to run the lsof command to see the
#     full output:
#         "/usr/bin/lsof -i"
#

sudo_ability() {
  # Do I have sudo access to the lsof command -i?
  /usr/bin/sudo -l | /usr/bin/grep "/usr/bin/lsof -i"; exit $?
}

ports(){
  /usr/bin/sudo /usr/bin/lsof -i; exit $?
}

#------#
# MAIN #
#------#

CMD=$1
ARGS=$2

case "$CMD" in
    sudo_ability)
        sudo_ability "$ARGS" 
        ;;
    ports)
        ports "$ARGS" 
        ;;
    *)
        echo "Unsupported command $CMD"
        exit 1
        ;;
esac
