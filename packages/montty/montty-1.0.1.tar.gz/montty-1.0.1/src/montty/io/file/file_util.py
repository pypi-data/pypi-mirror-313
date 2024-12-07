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

import os.path
import os
from glob import glob
import shutil
from montty.platform.config_values import ConfigValues


class FileUtil:

    # Exists

    @classmethod
    def exists(cls, file_path_name: str) -> bool:
        return os.path.exists(file_path_name)

    @classmethod
    def not_exists(cls, file_path_name: str) -> bool:
        return not os.path.isfile(file_path_name)

    # Create

    @classmethod
    def mkdir(cls, path):
        return os.mkdir(path)  # pragma: no cover

    @classmethod
    def touch(cls, path):
        with open(path, 'a', encoding=f"{ConfigValues.FILE_ENCODING}"):
            os.utime(path, None)

    # Copy

    @classmethod
    def copy_file(cls, from_file, to_file):
        shutil.copyfile(from_file, to_file)

    # Delete

    @classmethod
    def delete_file(cls, path):
        os.remove(path)

    @classmethod
    def delete_files(cls, file_paths):
        for file_path in file_paths:
            os.remove(file_path)

    @classmethod
    def delete_files_by_regex(cls, path_with_regex):
        for file in glob(path_with_regex):
            os.remove(file)
