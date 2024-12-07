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

from montty.io.file.file_util import FileUtil


class TestFile():
    ##########
    # Exists #
    ##########

    def test_exists_true(self):
        assert FileUtil.exists(__file__) is True

    def test_exists_false(self):
        assert FileUtil.exists(__file__+".bad") is False

    #################
    # Create/Delete #
    #################

    def test_touch(self, tmpdir):
        file_create = tmpdir.join("file_create")
        assert FileUtil.exists(file_create) is False
        assert len(tmpdir.listdir()) == 0

        FileUtil.touch(file_create)
        assert FileUtil.exists(file_create) is True
        assert len(tmpdir.listdir()) == 1

        FileUtil.delete_file(file_create)
        assert FileUtil.exists(file_create) is False
        assert len(tmpdir.listdir()) == 0

    ###############
    # Copy/Delete #
    ###############

    def test_copy(self, tmpdir):
        # Make file to copy
        file_copy_from = tmpdir.join("file_copy_from")
        FileUtil.touch(file_copy_from)
        assert FileUtil.exists(file_copy_from) is True
        assert len(tmpdir.listdir()) == 1

        # Copy the file
        file_copy_to = tmpdir.join("file_copy_to")
        FileUtil.copy_file(file_copy_from, file_copy_to)
        assert FileUtil.exists(file_copy_to) is True
        assert len(tmpdir.listdir()) == 2

        # Delete both files
        FileUtil.delete_files([file_copy_from, file_copy_to])
        assert FileUtil.exists(file_copy_from) is False
        assert FileUtil.exists(file_copy_to) is False
        assert len(tmpdir.listdir()) == 0

    ##########
    # Delete #
    ##########

    def test_delete_regex(self, tmpdir):
        # Create files to delete
        files = [
            tmpdir.join("file.tmp"),
            tmpdir.join("file_tmp1.txt"),
            tmpdir.join("tmp_file.txt"),
            tmpdir.join("tmp"),
            tmpdir.join("_tmp_"),
            tmpdir.join("no_match"),
        ]

        for file in files:
            FileUtil.touch(file)
            assert FileUtil.exists(file) is True
        assert len(tmpdir.listdir()) == 6

        # Delete the files by a matching regex, one file should not match
        # and hence not be deleted
        file_delete_regex = tmpdir.join('*tmp*')
        FileUtil.delete_files_by_regex(str(file_delete_regex))

        assert len(tmpdir.listdir()) == 1
        assert FileUtil.exists(files[-1]) is True
