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
from montty.app.check.file.check_file_parser import CheckFileParser


class DataCheckFile():
    @classmethod
    def setup_parser_with_root_and_one_base_class(cls):
        file_name = 'chk_2_base_classes.py'
        file_name_path = cls.get_full_file_path(file_name)
        check_file_parser = CheckFileParser.create_instance(file_name_path)
        return check_file_parser

    @classmethod
    def setup_parser_with_root_and_two_base_class(cls):
        file_name = 'chk_3_base_classes.py'
        file_name_path = cls.get_full_file_path(file_name)
        check_file_parser = CheckFileParser.create_instance(file_name_path)
        return check_file_parser

    @classmethod
    def setup_parser_with_multipe_root_classes(cls):
        file_name = 'chk_multi_root_classes.py'
        file_name_path = cls.get_full_file_path(file_name)
        check_file_parser = CheckFileParser.create_instance(file_name_path)
        return check_file_parser

    @classmethod
    def get_full_file_path(cls, file_name):
        return cls.get_location_of_data_files() + file_name

    @classmethod
    def get_location_of_data_files(cls):
        location = os.path.realpath(os.path.join(
            os.getcwd(), os.path.dirname(__file__)))
        data_path = location + "/data/"
        return data_path
