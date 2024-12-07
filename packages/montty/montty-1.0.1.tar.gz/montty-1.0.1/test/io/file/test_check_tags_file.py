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
import pytest
from montty.io.file.check_tags_file import CheckTagsFile


class TestCheckTagsFile():
    def _write_fixture_file_lines(self, file_name: str, multi_lines: list[str]):
        '''Write a single line for checks file csv file'''
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('check_file_name,tags\n')  # csv header
            for line in multi_lines:
                f.write(f'{line}\n')

    ###############
    # Single line #
    ###############

    def test_single_line_two_tags_select_first(self):
        file_name = 'file_single_line_two_tags_Select_first.csv'
        checks_file_lines = []
        checks_file_lines.append('chk_test.mty,tag_one tag_two')
        self._write_fixture_file_lines(file_name, checks_file_lines)

        check_tags_file = CheckTagsFile()
        check_tags_file.load_from_file(file_name)

        # Select first tag only
        check_tags_file.get_for_tag('tag_one')

        file_names: set[str] = check_tags_file.get_file_names()
        assert len(file_names) == 1
        assert file_names.pop() == 'chk_test.mty'
        os.remove(file_name)

    def test_single_line_two_tags_select_both(self):
        file_name = 'file_single_line_two_tags_select_both.csv'
        checks_file_lines = []
        checks_file_lines.append('chk_test.mty,tag_one tag_two')
        self._write_fixture_file_lines(file_name, checks_file_lines)

        check_tags_file = CheckTagsFile()
        check_tags_file.load_from_file(file_name)

        # Select both tags
        check_tags_file.get_for_tag('tag_one')
        check_tags_file.get_for_tag('tag_two')

        file_names: set[str] = check_tags_file.get_file_names()
        assert len(file_names) == 1
        assert file_names.pop() == 'chk_test.mty'
        os.remove(file_name)

    def test_line_format_single_space(self):
        file_name = 'file_line_format_single_space.csv'
        checks_file_lines = []
        checks_file_lines.append('chk_first.mty,tag_one tag_two')
        checks_file_lines.append('chk_second.mty, tag_three tag_four ')
        self._write_fixture_file_lines(file_name, checks_file_lines)

        # Case 1

        check_tags_file = CheckTagsFile()
        check_tags_file.load_from_file(file_name)

        # Select both tags
        check_tags_file.get_for_tag('tag_three')

        file_names: set[str] = check_tags_file.get_file_names()
        assert len(file_names) == 1
        assert 'chk_second.mty' in file_names

        # Case 2

        # Select both tags
        check_tags_file.get_for_tag('tag_one')
        check_tags_file.get_for_tag('tag_three')

        file_names: set[str] = check_tags_file.get_file_names()
        assert len(file_names) == 2
        assert 'chk_first.mty' in file_names
        assert 'chk_second.mty' in file_names

        os.remove(file_name)

    def test_line_format_multi_space(self):
        file_name = 'file_line_format_multi_space.csv'
        checks_file_lines = []
        checks_file_lines.append('chk_first.mty,  tag_one   tag_two  ')
        checks_file_lines.append('chk_second.mty,  tag_three   tag_four   ')
        self._write_fixture_file_lines(file_name, checks_file_lines)

        # Case 1

        check_tags_file = CheckTagsFile()
        check_tags_file.load_from_file(file_name)

        # Select both tags
        check_tags_file.get_for_tag('tag_three')

        file_names: set[str] = check_tags_file.get_file_names()
        assert len(file_names) == 1
        assert 'chk_second.mty' in file_names

        # Case 2

        # Select both tags
        check_tags_file.get_for_tag('tag_one')
        check_tags_file.get_for_tag('tag_three')

        file_names: set[str] = check_tags_file.get_file_names()
        assert len(file_names) == 2
        assert 'chk_first.mty' in file_names
        assert 'chk_second.mty' in file_names

        os.remove(file_name)

    ##############
    # Multi line #
    ##############

    def test_multi_line_multi_tags(self):
        file_name = 'file_multi_line_multi_tags.csv'
        checks_file_lines = []
        checks_file_lines.append('chk_002_python_host_cpu.py, python_check')
        checks_file_lines.append(
            'chk_003_cla_python_host_cpu_etc.py, collect_check collect_depend_check python_check')
        checks_file_lines.append(
            'chk_004_clf_bash_ss.py, collect_check collect_filter_check bash_check')
        checks_file_lines.append('chk_005_cld_bash_sudo_ufw.py, collect_check')
        checks_file_lines.append(
            'chk_006_cld_bash_data_sudo_lsof.py, collect_check')
        self._write_fixture_file_lines(file_name, checks_file_lines)

        check_tags_file = CheckTagsFile()
        check_tags_file.load_from_file(file_name)

        # Select both tags
        check_tags_file.get_for_tag('python_check')

        file_names: set[str] = check_tags_file.get_file_names()
        assert len(file_names) == 2
        assert 'chk_002_python_host_cpu.py' in file_names
        assert 'chk_003_cla_python_host_cpu_etc.py' in file_names
        os.remove(file_name)

    #########################
    # Utility/debug methods #
    #########################

    def test_file_dump_single_line(self):
        file_name = 'file_dump_single_line.csv'
        checks_file_lines = []
        checks_file_lines.append('chk_text.mty,tag_one tag_two')
        self._write_fixture_file_lines(file_name, checks_file_lines)

        check_tags_file = CheckTagsFile()
        result = check_tags_file.dump_file(file_name)
        assert result == 'chk_text.mty,tag_one tag_two\n'
        os.remove(file_name)

    def test_file_dump_multi_line(self):
        file_name = 'file_dump_multi_line.csv'
        checks_file_lines = []
        checks_file_lines.append('chk_test1.mty,tag_one tag_two')
        checks_file_lines.append('chk_test2.mty,tag_three tag_four')
        self._write_fixture_file_lines(file_name, checks_file_lines)

        check_tags_file = CheckTagsFile()
        result = check_tags_file.dump_file(file_name)
        assert result == 'chk_test1.mty,tag_one tag_two\nchk_test2.mty,tag_three tag_four\n'
        os.remove(file_name)

    ##################
    # Negative cases #
    ##################

    def test_non_existing_file(self):
        file_name = 'non_existing_file.csv'
        check_tags_file = CheckTagsFile()
        with pytest.raises(FileNotFoundError):
            check_tags_file.load_from_file(file_name)

    def test_dump_non_existing_file(self):
        file_name = 'non_existing_file.csv'
        check_tags_file = CheckTagsFile()
        with pytest.raises(FileNotFoundError):
            check_tags_file.dump_file(file_name)
