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

# PEP-8 format

autopep8 -r -i ../src
autopep8 -r -i ./

# Pylint linter - disable the following checks generally:
#
# C0103 - Invalid-name
# C0114 - Missing module docstring
# C0115 - Missing-class-docstring
# C0116 - Missing-function-docstring
# C0301 - Line-too-long
# R0801 - Duplicate-code
# R0903 - Too-few-public-methods
# W0719 - Broad-exception-raised 
#
# R1702 - Too many nested blocks
# R0904 - Too many public methods 
# R0912 - Too many branches
#

export PYTHONPATH=../src/montty/montty_deploy/CHECKS/PYTHON_LIBS
pylint --verbose --disable "C0103,C0114,C0115,C0116,C0301,R0801,R0903,R0904,R0912,R1702,W0719" --recursive y ../src/
pylint --verbose --disable "C0103,C0114,C0115,C0116,C0301,R0801,R0903,R0904,R0912,R1702,W0719" --recursive y ./


