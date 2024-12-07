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

import pytest
from montty.app.check.file.check_file_parser import CheckFileParser
from . data_check_file import DataCheckFile


class TestCheckFileParser():
    def test_file_parses_okay_root_another_base_class(self):
        check_file_parser = DataCheckFile.setup_parser_with_root_and_one_base_class()
        class_found = check_file_parser.parse()

        # Check module and class name of loaded class
        assert class_found.get_module_name() == 'chk_2_base_classes'
        assert class_found.get_class_name() == 'CheckSystemCollection'

        # The class should have two base classes:
        #     RootCheck identies the 'root' check (For when there are 'sub checks')
        #     CollectAllCheck is the base class for the check (collects 'sub checks')
        assert len(class_found.get_base_class_names()) == 2
        assert class_found.get_number_base_classes() == 2
        assert class_found.get_base_class_names()[0] == 'RootCheck'
        assert class_found.get_base_class_names()[1] == "CollectAllCheck"

        # Check we are parsing the class methods as well
        assert class_found.get_number_methods() == 2
        assert "__init__" in class_found.get_method_names()

        # Check the "to string" method working
        assert "CheckSystemCollection" in str(class_found)

    def test_file_parses_okay_root_two_other_base_class(self):
        # chk_3_base_classes.py
        check_file_parser = DataCheckFile.setup_parser_with_root_and_two_base_class()
        class_found = check_file_parser.parse()

        # Check module and class name of loaded class
        assert class_found.get_module_name() == "chk_3_base_classes"
        assert class_found.get_class_name() == "CheckFakeCollection"

        # The class should have three base classes:
        #     RootCheck identies the 'root' check (For when there are 'sub checks')
        #     CollectAllCheck is the base class for the check (collects 'sub checks')
        #     SOmeOtherFakeClass is just some other class, happen to inherit from
        assert len(class_found.get_base_class_names()) == 3
        assert class_found.get_number_base_classes() == 3
        assert class_found.get_base_class_names()[0] == "RootCheck"
        assert class_found.get_base_class_names()[1] == "CollectAllCheck"
        assert class_found.get_base_class_names()[2] == "SomeOtherFakeClass"

        # Check we are parsing the class methods as well
        assert class_found.get_number_methods() == 2
        assert '__init__' in class_found.get_method_names()

        # Check the "to string" method working
        assert 'CheckFakeCollection' in str(class_found)

    def test_dump_parser_for_debugging(self):
        check_file_parser = DataCheckFile.setup_parser_with_root_and_one_base_class()
        string_dump = check_file_parser.dump()
        assert "CheckSystemCollection" in string_dump

    # Negative cases

    def test_bad_file_name(self):
        with pytest.raises(Exception) as emessage:
            CheckFileParser("/some/path/fake.bad", "")
        assert str(emessage.value) == "Cannot extract filename"

    def test_empty_file(self):
        check_file_parser = CheckFileParser("/some/path/fake.py", "")
        with pytest.raises(Exception) as emessage:
            check_file_parser.parse()
        assert str(
            emessage.value) == 'No root check class found, must be one (and only one)'

    def test_muliple_root_check_classes(self):
        with pytest.raises(Exception) as emessage:
            check_file_parser = DataCheckFile.setup_parser_with_multipe_root_classes()
            check_file_parser.parse()
        assert str(
            emessage.value) == "More than 1 root check class found, must be only one. Found ['CheckFakeCollection1', 'CheckFakeCollection2']"
