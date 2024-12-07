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

import curses
from montty.platform.config_values import ConfigValues
from montty.app.status import Status


class Screen:
    def __init__(self, montty_version: str):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self._montty_version = montty_version
        self.screen.keypad(True)
        self.screen.nodelay(True)
        self.header = None
        self.body = None
        self.screen_body_lines = []
        self.screen_max_body_lines = 21

    def shutdown(self):
        curses.nocbreak()
        curses.echo()
        self.screen.keypad(False)
        curses.endwin()

    # Keyboard

    # Skip from pytest coverage - not feasible to test
    def get_key(self):             # pragma: no cover
        key = self.screen.getch()  # pragma: no cover
        return key                 # pragma: no cover

    # Output management

    def clear(self):
        self.screen.clear()

    def paint(self):
        self.screen.refresh()

    def sleep_secs(self, seconds):
        curses.napms(seconds*1000)

    def sleep_millis(self, milli_seconds):
        curses.napms(milli_seconds)

    # Output

    def do_note(self, text):
        blank_text = "                                        "
        self.screen.addstr(1, 51, f"{blank_text:<40}", curses.A_DIM)
        self.screen.addstr(1, 51, f"{text:<40}", curses.A_DIM)

    def set_header(self, header):
        self.header = header

    def set_body(self, body):
        self.body = body

    # Header

    def write_header_startup(self):
        #                  Y  X
        self.screen.addstr(
            0, 0, ""+ConfigValues.LOGO+" ", curses.A_DIM | curses.A_ITALIC)
        self.screen.addstr(0, 10, "Awaiting report(s)")
        self.screen.addstr(1, 0, f"{self._montty_version}", curses.A_DIM)
        self.screen.addstr(1, 10, "[q]uit", curses.A_DIM)
        self.screen.addstr(1, 19,  "[^s]pause", curses.A_DIM)
        self.screen.addstr(1, 30, "[^q]resume", curses.A_DIM)
        # Display license text
        license_line_no = 3
        for license_line_text in ConfigValues.LICENSE_TEXT:
            self.screen.addstr(license_line_no, 10,
                               license_line_text, curses.A_DIM)
            license_line_no += 1

    def write_header_no_file(self):
        #                  Y  X
        self.screen.addstr(
            0, 0, ""+ConfigValues.LOGO+" ", curses.A_DIM | curses.A_ITALIC)
        self.screen.addstr(0, 10, "Awaiting report(s)")
        self.screen.addstr(1, 0, f"{self._montty_version}", curses.A_DIM)
        self.screen.addstr(1, 10, "[q]uit", curses.A_DIM)
        # Display license text
        # license_line_no = 3
        # for license_line_text in ConfigValues.LICENSE_TEXT:
        #    self.screen.addstr(license_line_no, 10,
        #                       license_line_text, curses.A_DIM)
        #    license_line_no += 1

    def write_header(self):
        # Logo

        self.screen.addstr(
            0, 0, ""+ConfigValues.LOGO+" ", curses.A_DIM | curses.A_ITALIC)

        # Status

        status = str(self.header.get_subject().get_status().get_str())
        if status in [Status.ALERT, Status.WARN]:
            self.screen.addstr(0, 10, status, curses.A_STANDOUT)
        else:
            self.screen.addstr(0, 10, status)

        # Host:

        host_x = 16
        self.screen.addstr(
            0, host_x, "Host: ", curses.A_DIM)
        self.screen.addstr(0, host_x+6,
                           str(self.header.get_subject().get_hostname()), curses.A_DIM)

        # IP:

        ip_x = host_x+23
        self.screen.addstr(
            0, ip_x, "IPv4: ", curses.A_DIM)
        self.screen.addstr(0, ip_x+6,
                           str(self.header.get_subject().get_ip()), curses.A_DIM)

        # At:

        at_x = ip_x+23
        self.screen.addstr(
            0, at_x, "At: ", curses.A_DIM)
        self.screen.addstr(
            0, at_x+4, str(self.header.get_subject().get_at()), curses.A_DIM)

    def write_header_menu_for_report(self):
        #                  Y  X
        self.screen.addstr(1, 0, f"{self._montty_version}", curses.A_DIM)
        quit_x = 10
        delete_x = quit_x+7
        pause_x = delete_x+9
        resume_x = pause_x+10
        self.screen.addstr(1, quit_x,   "[q]uit", curses.A_DIM)
        self.screen.addstr(1, delete_x, "[d]elete", curses.A_DIM)
        self.screen.addstr(1, pause_x,  "[^s]pause", curses.A_DIM)
        self.screen.addstr(1, resume_x, "[^q]resume", curses.A_DIM)

    def write_body(self):
        start_y = 3
        limit_body = 1
        for line in self.body.get_body():
            self.screen.addstr(start_y, 0, line)
            start_y = start_y + 1
            limit_body = limit_body + 1
            if limit_body >= self.screen_max_body_lines:
                break

    def clear_body_lines(self):
        self.screen_body_lines = []

    def append_body_line(self, line):
        self.screen_body_lines.append(line)
        if len(self.screen_body_lines) >= self.screen_max_body_lines:
            self.screen_body_lines.pop(0)

    def write_body_lines(self):
        start_y = 3
        limit_body = 1
        blank = "                                                                                                  "
        for line in self.screen_body_lines:
            self.screen.addstr(start_y, 0, blank)
            if f"({Status.ALERT})" in line or f"({Status.WARN})" in line:
                self.screen.addstr(start_y, 0, line, curses.A_STANDOUT)
            elif f"({Status.OKAY})" in line or f"({Status.NA})" in line:
                self.screen.addstr(start_y, 0, line, curses.A_DIM)
            elif line.startswith("SUMMARY"):
                status = self.header.get_subject().get_status()
                if status.is_alert() or status.is_warn():
                    self.screen.addstr(start_y, 0, line, curses.A_STANDOUT)
                else:
                    self.screen.addstr(start_y, 0, line, curses.A_DIM)
            else:
                self.screen.addstr(start_y, 0, "    " + line, curses.A_DIM)

            start_y = start_y + 1

            limit_body = limit_body + 1
            if limit_body >= self.screen_max_body_lines:
                break
