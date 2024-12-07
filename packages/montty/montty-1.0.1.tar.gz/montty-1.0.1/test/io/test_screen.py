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

from montty.report.body import Body
from montty.io.screen import Screen


TEST_MONTTY_VERSION_NUMBER = '1.0.0'


class TestScreen():

    def test_screen__body_from_text(self, fixture_test_header_status_okay, fixture_body_text_25):
        try:
            screen = Screen(TEST_MONTTY_VERSION_NUMBER)
            screen.clear()

            screen.set_header(fixture_test_header_status_okay)
            screen.do_note("TEST NOTE")

            body = Body()
            body.set_from_text(fixture_body_text_25)
            screen.set_body(body)

            screen.write_header_no_file()
            screen.write_header_menu_for_report()

            # Write body
            screen.write_body()

            screen.paint()
            screen.sleep_secs(2)
            screen.shutdown()
        finally:
            screen.shutdown()

    ###############
    # Body append #
    ###############

    # NA

    def test_screen__body_from_append_status_na(self, fixture_test_header_status_na, fixture_body_text_50):
        try:
            screen = Screen(TEST_MONTTY_VERSION_NUMBER)
            screen.clear()

            screen.set_header(fixture_test_header_status_na)
            screen.write_header()
            screen.write_header_menu_for_report()

            screen.do_note("TEST NOTE")

            body = Body()
            body.set_from_text(fixture_body_text_50)
            screen.set_body(body)

            # Write body lines
            screen.clear_body_lines()
            for line in body.get_body():
                screen.append_body_line(line)
                screen.write_body_lines()
                screen.paint()
                screen.sleep_millis(150)

            screen.paint()
            screen.sleep_secs(2)
            screen.shutdown()
        finally:
            screen.shutdown()

    # OKAY

    def test_screen__body_from_append_status_okay(self, fixture_test_header_status_okay, fixture_body_text_50):
        try:
            screen = Screen(TEST_MONTTY_VERSION_NUMBER)
            screen.clear()

            screen.set_header(fixture_test_header_status_okay)
            screen.write_header()
            screen.write_header_menu_for_report()

            # screen.do_note("TEST NOTE")

            body = Body()
            body.set_from_text(fixture_body_text_50)
            screen.set_body(body)

            # Write body lines
            screen.clear_body_lines()
            for line in body.get_body():
                screen.append_body_line(line)
                screen.write_body_lines()
                screen.paint()
                screen.sleep_millis(150)

            screen.paint()
            screen.sleep_secs(2)
            screen.shutdown()
        finally:
            screen.shutdown()

    # WARN

    def test_screen__body_from_append_status_warn(self, fixture_test_header_status_warn, fixture_body_text_50):
        try:
            screen = Screen(TEST_MONTTY_VERSION_NUMBER)
            screen.clear()

            screen.set_header(fixture_test_header_status_warn)
            screen.write_header()
            screen.write_header_menu_for_report()

            screen.do_note("TEST NOTE")

            body = Body()
            body.set_from_text(fixture_body_text_50)
            screen.set_body(body)

            # Write body lines
            screen.clear_body_lines()
            for line in body.get_body():
                screen.append_body_line(line)
                screen.write_body_lines()
                screen.paint()
                screen.sleep_millis(150)

            screen.paint()
            screen.sleep_secs(2)
            screen.shutdown()
        finally:
            screen.shutdown()

    # ALERT

    def test_screen__body_from_append_status_alert(self, fixture_test_header_status_alert, fixture_body_text_50):
        try:
            screen = Screen(TEST_MONTTY_VERSION_NUMBER)
            screen.clear()

            screen.set_header(fixture_test_header_status_alert)
            screen.write_header()
            screen.write_header_menu_for_report()

            # screen.do_note("TEST NOTE")

            body = Body()
            body.set_from_text(fixture_body_text_50)
            screen.set_body(body)

            # Write body lines
            screen.clear_body_lines()
            for line in body.get_body():
                screen.append_body_line(line)
                screen.write_body_lines()
                screen.paint()
                screen.sleep_millis(150)

            screen.paint()
            screen.sleep_secs(2)
            screen.shutdown()
        finally:
            screen.shutdown()
