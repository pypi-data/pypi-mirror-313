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

from montty.app.manager.manager_app import ManagerApp
from montty.montty_meta import MonttyMeta
from montty.platform.config_values import ConfigValues


def main():
    # License and version
    for license_line_text in ConfigValues.LICENSE_TEXT:
        print(license_line_text)
    print()

    montty_version = MonttyMeta().get_version()
    print(f"{ConfigValues.LOGO} Manager {montty_version} running ...\n")

    manager_app = ManagerApp()
    manager_app.accept_new_reports()

    # Remove expired
    manager_app.remove_expired_warn_reports()
    manager_app.remove_expired_okay_and_na_reports()

    # Requested deletes
    manager_app.remove_nas_requested_delete()
    manager_app.remove_okays_requested_delete()
    manager_app.remove_warns_requested_delete()
    manager_app.remove_alerts_requested_delete()


if __name__ == '__main__':
    main()
