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

# Run shellcheck scanner, which installs by:
#
#   debian:
#     sudo apt update
#     sudo apt install shellcheck
#
#   rhel:
#     sudo dnf update
#     sudo dnf install ShellCheck
#
#   arch:
#     sudo pacman -Syu
#     sudo pacman -S shellcheck
#

clear

echo "Run shellcheck on bash scripts under CHECKS/BASH_SCRIPTS"

# Cd into where the bash scripts to be tested should be

current_dir=$(pwd)

cd ../CHECKS/BASH_SCRIPTS || exit
shellcheck -x ./*.sh

cd ./mty_util || exit
shellcheck -x ./*.sh

cd "${current_dir}" || exit
cd ../src/montty/montty_deploy || exit
shellcheck -x ./*.sh

echo ""
