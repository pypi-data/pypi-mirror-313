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

import argparse
import os
import shutil
from montty.io.dir.install_dir import InstallDir
from montty.io.file.file_util import FileUtil
from montty.montty_meta import MonttyMeta
from montty.platform.config_values import ConfigValues
from montty.montty_deploy.deploy_dir import DeployDir


class CopyItem:
    def __init__(self, deploy_dir, install_dir, name):
        self._name = name
        self._exists = None
        self._copy_from = deploy_dir.get_path() + "/" + name
        self._copy_to = install_dir.get_path() + "/" + name

    def exists(self):
        self._exists = FileUtil.exists(self._copy_to)
        if self._exists:
            print(f"    {self._name:18} exists")
        else:
            print(f"    {self._name:18} NOT exist")

    def get_exists(self):
        return self._exists

    def copy(self):
        print(f"    COPYING: {self._name}")
        print(f"                       from -> {self._copy_from}")
        print(f"                       to   -> {self._copy_to}")


class CopyFile(CopyItem):
    def __init__(self, deploy_dir, install_dir, name, is_executable):
        super().__init__(deploy_dir, install_dir, name)
        self._is_executable = is_executable

    def copy(self):
        super().copy()
        shutil.copyfile(self._copy_from, self._copy_to)
        if self._is_executable:
            os.chmod(self._copy_to, 0o744)


class CopyDir(CopyItem):
    def copy(self):
        super().copy()
        shutil.copytree(self._copy_from, self._copy_to)


class CopyFiles:
    def __init__(self):
        self._deploy_dir = DeployDir()
        self._install_dir = InstallDir.create_instance()
        self._copy_files = []
        self._copy_dirs = []

    # FILES

    def add_file(self, name, is_executable):
        self._copy_files.append(
            CopyFile(self._deploy_dir, self._install_dir, name, is_executable))

    def files_exist(self):
        print("  Exist/Not Exist:")
        for file in self._copy_files:
            file.exists()

    def files_copy(self):
        print("  Copying:")
        file_copied = False
        for copy_file in self._copy_files:
            if not copy_file.get_exists():
                file_copied = True
                copy_file.copy()
        if not file_copied:
            print("    No files were copied, they all exist ...")

    # DIRs

    def add_dir(self, name):
        self._copy_dirs.append(
            CopyDir(self._deploy_dir, self._install_dir, name))

    def dirs_exist(self):
        print("  Exist/Not Exist:")
        for copy_dir in self._copy_dirs:
            copy_dir.exists()

    def dirs_copy(self):
        print("  Copying:")
        dir_copied = False
        for copy_dir in self._copy_dirs:
            if not copy_dir.get_exists():
                dir_copied = True
                copy_dir.copy()
        if not dir_copied:
            print("    No directories were copied, they all exist ...")


def main():
    # License and version
    for license_line_text in ConfigValues.LICENSE_TEXT:
        print(license_line_text)
    print()

    montty_version = MonttyMeta().get_version()
    print(f"{ConfigValues.LOGO} Deployer {montty_version} running ...\n")

    # Handle argument(s)
    parser = argparse.ArgumentParser(
        description='Initial deployer script for MonTTY, to prepare the project directory.')
    parser.parse_args()

    copy_files = CopyFiles()

    print("\n[Files]:")
    copy_files.add_file("run.sh", True)
    copy_files.add_file("spy.sh", True)
    copy_files.files_exist()
    copy_files.files_copy()

    print("\n[Directories]:")
    copy_files.add_dir("CHECKS")
    copy_files.add_dir("REPORTS")
    copy_files.dirs_exist()
    copy_files.dirs_copy()


if __name__ == "__main__":
    main()
