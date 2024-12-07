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
import shutil
from montty.app.monitor.monitor_app import MonitorApp
from montty.io.screen import Screen
from montty.io.file.file_util import FileUtil
from montty.io.file.file_reader import FileReader
from montty.io.file.file_name import MonttyFileName
from montty.montty_meta import MonttyMeta
from montty.platform.config_values import ConfigValues


def check_terminal_size(min_width=ConfigValues.TERMINAL_MIN_WIDTH, min_height=ConfigValues.TERMINAL_MIN_HEIGHT):
    # Get terminal size
    size = shutil.get_terminal_size((min_width, min_height))
    width, height = size.columns, size.lines

    # Check if terminal size meets minimum requirements
    if width < min_width or height < min_height:
        print(
            f"Error: Terminal size too small. Minimum required: {min_width}x{min_height}, but got: {width}x{height}.")
        sys.exit(1)  # Exit the program with an error status


LINE_SPEED_MILLIS_STD = 150
LINE_SPEED_MILLIS_RAPID = 10


class MonitorView:
    def __init__(self, monitor_app):
        self._montty_meta = MonttyMeta()
        self._montty_version = self._montty_meta.get_version()
        self._line_speed_millis = LINE_SPEED_MILLIS_STD
        self.monitor_app = monitor_app
        check_terminal_size()

        self.screen = Screen(self._montty_version)
        self.screen.clear()

    def set_line_speed_std(self):
        self._line_speed_millis = LINE_SPEED_MILLIS_STD

    def set_line_speed_rapid(self):
        self._line_speed_millis = LINE_SPEED_MILLIS_RAPID

    def display_startup(self):
        self.screen.clear()
        self.screen.write_header_startup()
        self.screen.paint()
        self.screen.sleep_millis(5000)
        self.handle_keypress()

    def display_clear(self):
        self.screen.clear()

    def display_no_file(self):
        # self.screen.clear()
        self.screen.write_header_no_file()
        self.screen.paint()
        self.screen.sleep_millis(2000)
        self.handle_keypress()

    def display_current_file(self):
        self.set_line_speed_std()

        self.screen.clear()
        montty_file = self.monitor_app.get_next_file()
        if montty_file and FileUtil.exists(montty_file):
            # Read montty file
            file_reader = FileReader(montty_file)
            file_reader.read()
            header = file_reader.get_header()
            body = file_reader.get_body()
            montty_file_guid = MonttyFileName.extract_guid(montty_file)

            # Display report GUID
            self.screen.do_note("Report: " + montty_file_guid)

            # Display to screen
            self.screen.set_header(header)
            self.screen.set_body(body)
            self.screen.write_header()

            self.screen.write_header_menu_for_report()
            self.screen.paint()
            self.screen.clear_body_lines()

            montty_file_status = MonttyFileName.extract_status(montty_file)

            for line in body.get_body():
                self.screen.append_body_line(line)
                self.screen.write_body_lines()
                self.screen.paint()
                self.handle_keypress(montty_file_guid, montty_file_status)
                self.screen.sleep_millis(self._line_speed_millis)

            # Delay at end of paint of screen, to let user absorb info
            # in the summary section
            for _ in range(1, 15):
                self.screen.paint()
                self.handle_keypress(montty_file_guid, montty_file_status)
                self.screen.sleep_millis(self._line_speed_millis)

    def shutdown(self):
        self.screen.shutdown()

    def handle_keypress(self, montty_file_guid=None, montty_file_status=None):
        key = self.screen.get_key()
        if key == ord('q'):
            self.screen.do_note("Quiting ...")
            self.screen.paint()
            self.screen.sleep_secs(1)
            self.screen.shutdown()
            sys.exit()
        elif key == ord('d') and montty_file_guid:
            self.screen.do_note("Report: <DELETE> " + montty_file_guid)
            self.screen.paint()
            # Request file be deleted
            self.monitor_app.add_request_delete_file(
                montty_file_guid, montty_file_status)

            self.set_line_speed_rapid()


def main():
    monitor_app = MonitorApp()
    monitor_view = MonitorView(monitor_app)

    monitor_view.display_startup()
    monitor_view.display_clear()
    require_display_clear = False

    # Display loop
    while True:
        monitor_app.update_next_file()

        # Handle no available reports
        if not monitor_app.has_next_file():
            if require_display_clear:
                require_display_clear = False
                monitor_view.display_clear()
            monitor_view.display_no_file()
        else:
            require_display_clear = True
            monitor_view.display_current_file()

    monitor_view.shutdown()
