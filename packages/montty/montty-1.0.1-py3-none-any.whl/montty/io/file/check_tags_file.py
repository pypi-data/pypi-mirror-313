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

import csv
from montty.io.dir.checks_dir import ChecksDir
from montty.io.file.file_util import FileUtil
from montty.platform.config_values import ConfigValues


class FileRow:
    def __init__(self, file_name: str, tags: list[str]):
        self._file_name = file_name
        self._tags = tags

    def file_name(self):
        return self._file_name

    def has_tag(self, tag):
        if tag in self._tags:
            return True
        return False


class CheckTagsFile:
    '''Load check file names from a "check file", for given tag(s)

    Usage:
        <instance>.load()
        for tag in requested_check_tags:
             <instance>.get_for_tag(tag)

        check_file_names = <instance>.get_file_names()

        You now have all the "check file names" for the given tags
    '''

    def __init__(self):
        self._file_rows: list[FileRow] = []
        self._file_names: set[str] = set()

    def load(self):  # pragma: no cover
        checks_dir = ChecksDir()
        self.load_from_file(checks_dir.get_checks_file_path())

    def dump_file(self, file_path_name: str) -> str:
        if FileUtil.not_exists(file_path_name):
            raise FileNotFoundError(
                f"The file {file_path_name} does not exist")

        result = ""
        with open(file_path_name, mode='r', newline='', encoding=f"{ConfigValues.FILE_ENCODING}") as file:
            reader = csv.DictReader(file)
            for row in reader:
                result += f"{row['check_file_name']},{row['tags']}\n"
        return result

    def load_from_file(self, file_path_name: str) -> None:
        if FileUtil.not_exists(file_path_name):
            raise FileNotFoundError(
                f"The file {file_path_name} does not exist")

        with open(file_path_name, mode='r', newline='', encoding=f"{ConfigValues.FILE_ENCODING}") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Accessing the values in each row
                file_name = row['check_file_name']

                # Remove quotes and split tags
                tags = row['tags'].strip('"').split()
                self._file_rows.append(FileRow(file_name, tags))

    def get_for_tag(self, tag) -> set[str]:
        for file_row in self._file_rows:
            if file_row.has_tag(tag):
                self._file_names.add(file_row.file_name())

    def get_file_names(self) -> set[str]:
        return self._file_names
