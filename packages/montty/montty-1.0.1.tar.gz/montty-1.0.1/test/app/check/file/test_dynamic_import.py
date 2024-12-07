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

import sys
from montty.app.check.file.dynamic_import import DynamicImport
from . data_check_file import DataCheckFile


class TestDynamicImport:
    def _setup(self):
        check_file_parser = DataCheckFile.setup_parser_with_root_and_one_base_class()
        return check_file_parser

    def test_dynamic_import(self):
        module_dir = DataCheckFile.get_location_of_data_files()
        sys.path.append(module_dir)

        check_file_parser = self._setup()
        class_found = check_file_parser.parse()
        module_name = class_found.get_module_name()
        class_name = class_found.get_class_name()

        dynamic_import = DynamicImport(module_name, class_name)
        my_instance = dynamic_import.get_instance()
        my_instance.run()
        output = my_instance.get_output()
        assert "chk_2_base_classes" in output
