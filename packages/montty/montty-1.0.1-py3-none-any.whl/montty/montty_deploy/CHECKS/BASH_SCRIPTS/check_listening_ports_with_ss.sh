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

# Above "shebang" not actually needed, only used to communicate this is a BaSH
# script, to people, and to utilities like "shellcheck"

# Check Listening Sockets
# -----------------------
#
# Contrived example, using the Linux "ss" command to check is any listening
# sockets are "allowed"
#
# ss command:
#    ss -Hltp
#      ss  - Utility to investigate sockets.
#        -H: Hides the column headers in the output.
#        -l: Lists listening sockets.
#        -t: Displays TCP sockets.
#        -p: Shows the process using the socket.
#
# Also again contrived to demonstrate calls to MonTTY supplied BaSH scripts, to
# determine the hostname and vary the "allowed listening sockets" depending on the
# hostname

# Determine current directory (_dir), so we can subsequently call other BaSH scripts.
# Need to do this, as MonTTY does not add the BASH_SCRIPTS directory to the PATH. This
# is for security reasons - to not rely on the shell PATH for MonTTY scripts access

_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine if our host is one that should not allow ssh port listening
# Two command possibilities, first does not discard the output from mtyhost, the
# second form does discard the output. Use whichever form you prefer

ssh_not_allowed=$("${_dir}"/mty_util/mtyhost.sh host_in "fakehost1\nfakehost2\n"); ssh_not_allowed=$?

if [ "$ssh_not_allowed" -eq 0 ] ;
then
  # ssh not allowed on host
  "${_dir}"/mty_util/mtyss.sh -Hltp | /usr/bin/sed '/:domain\|:ipp/d' | tee /dev/fd/2 | /usr/bin/grep -q . && exit 1 || exit 0
else
  # ssh allowed on host
  "${_dir}"/mty_util/mtyss.sh -Hltp | /usr/bin/sed '/:domain\|:ipp\|:ssh/d' | tee /dev/fd/2 | /usr/bin/grep -q . && exit 1 || exit 0
fi
