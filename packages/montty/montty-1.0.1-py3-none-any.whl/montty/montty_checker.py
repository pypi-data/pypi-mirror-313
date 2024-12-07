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
import sys
from montty.app.check.check_app import CheckApp
from montty.io.file.check_tags_file import CheckTagsFile
from montty.montty_meta import MonttyMeta
from montty.platform.config_values import ConfigValues


def main():
    # Takes 1 argument, which is "tags"

    parser = argparse.ArgumentParser()
    parser.add_argument('tags')
    args = parser.parse_args()
    if len(args.tags) > ConfigValues.CHECK_APP_MAX_TAGS_PARAM_LEN:
        raise ValueError(
            "Argument tags must have a length <= {ConfigValues.CHECK_APP_MAX_TAGS_PARAM_LEN:}")

    requested_check_tags = args.tags.split()

    # License and version
    for license_line_text in ConfigValues.LICENSE_TEXT:
        print(license_line_text)
    print()

    montty_version = MonttyMeta().get_version()
    print(f"{ConfigValues.LOGO} Checker {montty_version} running ...\n")

    check_app = CheckApp()

    # For dynamic class import
    sys.path.append(check_app.get_check_dir_path())

    # For user supplied Python libraries
    sys.path.append(check_app.get_check_dir_path_python_libs_dir())

    if len(requested_check_tags) == 0:
        # No tags specified - load all checks
        check_app.add_all_check_files()
    else:
        # Requested check tags specified - load only checks that have
        # at least one of the tag(s)
        check_tags_file = CheckTagsFile()
        check_tags_file.load()
        for tag in requested_check_tags:
            check_tags_file.get_for_tag(tag)

        check_file_names = check_tags_file.get_file_names()
        check_app.add_specific_check_files(check_file_names)

    check_app.sort_checks()
    check_app.run_checks()
    check_app.build_report()


if __name__ == '__main__':
    main()
