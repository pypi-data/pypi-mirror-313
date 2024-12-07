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
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

clear

echo "Check directories that have a .py file, also have a __init__.py file"

# Check directories that have a .py file, also have a __init__.py file
#
#../src
echo ""
echo "SRC dirs ..."
echo ""
cd ../src; find . -type d -exec sh -c 'if [ -n "$(find "$1" -maxdepth 1 -name "*.py" | grep -v "__init__.py")" ] && [ ! -e "$1/__init__.py" ]; then echo "$1"; fi' sh {} \;

# Here for 'test'
echo ""
echo "TEST dirs ..."
echo ""
find . -type d -exec sh -c 'if [ -n "$(find "$1" -maxdepth 1 -name "*.py" | grep -v "__init__.py")" ] && [ ! -e "$1/__init__.py" ]; then echo "$1"; fi' sh {} \;

echo ""
