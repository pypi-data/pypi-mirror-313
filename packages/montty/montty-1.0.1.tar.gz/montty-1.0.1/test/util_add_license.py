#!/usr/bin/env python

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
from montty.platform.config_values import ConfigValues


def add_license_header_to_file(file_path, license_header):
    with open(file_path, 'r+', encoding="utf-8") as file:
        content = file.read()
        # Only add the header if it's not already present
        if not content.startswith(license_header):
            file.seek(0)  # Move to the beginning of the file
            file.write(license_header + '\n' + content)


def add_license_header_to_directory(directory, file_ext, license_header):
    # for root, dirs, files in os.walk(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(file_ext):
                file_path = os.path.join(root, file)
                add_license_header_to_file(file_path, license_header)
                # print(f'{file_path}\n')


def main():
    # directory_path = '../src/montty'
    directory_path = '../src/montty_deploy'
    # directory_path = '.'
    file_ext = '.sh'

    license_header = '\n'.join(
        f'# {license_line_text}' for license_line_text in ConfigValues.LICENSE_TEXT) + '\n'

    print(license_header)

    add_license_header_to_directory(directory_path, file_ext, license_header)


if __name__ == "__main__":
    main()
