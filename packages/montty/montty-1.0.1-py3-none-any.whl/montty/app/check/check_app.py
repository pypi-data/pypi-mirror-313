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

from montty.app.check.file.check_file_parser import CheckFileParser
from montty.app.check.file.dynamic_import import DynamicImport
from montty.app.status import Status
from montty.io.dir.checks_dir import ChecksDir
from montty.io.dir.python_libs_dir import PythonLibsDir
from montty.io.dir.reports_dir import ReportsDir
from montty.io.file.file_writer import FileWriter
from montty.io.file.file_name import MonttyFileName
from montty.platform.platform_values import PlatformValues
from montty.report.subject import Subject
from montty.report.header import Header
from montty.report.body import Body


class CheckApp():
    def __init__(self):
        # Checks
        self._checks_dir = ChecksDir()
        self._python_libs_dir = PythonLibsDir()
        self._checks = []
        self._checks_output = ""
        self._checks_output_summary = "\n\nSUMMARY:\n\n"
        # Start off assuming the check is "na"
        self._status = Status.create_na()

    # Checks

    def get_check_dir_path(self):
        return self._checks_dir.get_path()

    def get_check_dir_path_python_libs_dir(self):
        return self._python_libs_dir.get_path()

    def get_check_dir_files(self):
        return self._checks_dir.get_python_check_files()

    def add_check(self, check):
        self._checks.append(check)

    def sort_checks(self):
        self._checks.sort()

    def run_checks(self):
        # Run the checks
        first = True
        for check in self._checks:
            check.run()

            # Update this app status from check
            self._status.merge(check.get_status())

            # Add spacer for non first check outputs
            if not first:
                self._checks_output += "\n"
            else:
                first = False
            self._checks_output += check.get_output()
            self._checks_output_summary += '     ' + \
                check.get_output().partition('\n')[0] + '\n'

    def build_report(self):
        reports_dir = ReportsDir()
        subject = Subject()

        if self._status.is_alert():
            subject.set_status_alert()
            file_name = MonttyFileName.create_file_name_alert()
        elif self._status.is_warn():
            subject.set_status_warn()
            file_name = MonttyFileName.create_file_name_warn()
        elif self._status.is_okay():
            subject.set_status_okay()
            file_name = MonttyFileName.create_file_name_okay()
        else:
            subject.set_status_na()
            file_name = MonttyFileName.create_file_name_na()

        full_file_name = reports_dir.get_input_dir_path()+file_name

        # Build subject
        subject.set_hostname(PlatformValues.get_hostname())
        subject.set_ip(PlatformValues.get_ip())
        subject.set_at_now()
        file_writer = FileWriter(full_file_name)
        file_writer.set_header(Header(subject))

        # Build body
        body = Body()
        body.set_from_text(self._checks_output + self._checks_output_summary)
        file_writer.set_body(body)

        # Write file
        file_writer.write()

    ###############
    # Load checks #
    ###############

    def add_all_check_files(self):
        check_files = self.get_check_dir_files()
        check_files.sort()

        for check_file_name in check_files:
            check_file_parser = CheckFileParser.create_instance(
                check_file_name)
            class_found = check_file_parser.parse()
            module_name = class_found.get_module_name()
            class_name = class_found.get_class_name()

            dynamic_import = DynamicImport(module_name, class_name)
            my_instance = dynamic_import.get_instance()

            # Add checks to be run
            self.add_check(my_instance)

    def add_specific_check_files(self, check_files_to_load: list[str]):
        checks_dir = ChecksDir()

        for check_file_name in check_files_to_load:
            full_check_file_name = checks_dir.get_check_file_path(
                check_file_name)

            check_file_parser = CheckFileParser.create_instance(
                full_check_file_name)
            class_found = check_file_parser.parse()
            module_name = class_found.get_module_name()
            class_name = class_found.get_class_name()

            dynamic_import = DynamicImport(module_name, class_name)
            my_instance = dynamic_import.get_instance()

            # Add checks to be run
            self.add_check(my_instance)
