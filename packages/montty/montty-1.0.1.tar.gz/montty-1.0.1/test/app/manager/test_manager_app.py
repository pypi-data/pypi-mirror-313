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

from . data_manager_app import DataManagerApp


class TestManagerApp():
    def test_initial_state(self):
        DataManagerApp.setup()

    ###################
    # NA file expires #
    ###################

    def test_input_of_na_status_file__expires(self):
        manager_app = DataManagerApp.setup()

        # Create in _input dir - an NA file
        DataManagerApp.create_input_dir_file_na1()

        # Manager moves it to the _report dir
        manager_app.accept_new_reports()
        assert DataManagerApp.exists_report_dir_file_na1()

        # Now remove it as it should be expired
        manager_app.remove_expired_okay_and_na_reports()
        assert not DataManagerApp.exists_report_dir_file_na1()

    #####################
    # OKAY file expires #
    #####################

    def test_input_of_okay_status_file__expires(self):
        manager_app = DataManagerApp.setup()

        # Create in _input dir - an OKAY file
        DataManagerApp.create_input_dir_file_okay1()

        # Manager moves it to the _report dir
        manager_app.accept_new_reports()
        assert DataManagerApp.exists_report_dir_file_okay1()

        # Now remove it as it should be expired
        manager_app.remove_expired_okay_and_na_reports()
        assert not DataManagerApp.exists_report_dir_file_okay1()

    #####################
    # WARN file expires #
    #####################

    def test_input_of_warn_status_file__expires(self):
        manager_app = DataManagerApp.setup()

        # Create in _input dir - a WARN file
        DataManagerApp.create_input_dir_file_warn1()

        # Manager moves it to the _warn dir
        manager_app.accept_new_reports()
        assert DataManagerApp.exists_warn_dir_file_warn1()

        # No "close file" yet for warn - so warn not removed
        manager_app.remove_expired_okay_and_na_reports()
        assert DataManagerApp.exists_warn_dir_file_warn1()

        # Now remove it as it should be expired
        manager_app.remove_expired_warn_reports()
        assert not DataManagerApp.exists_warn_dir_file_warn1()

    #########
    # CLOSE #
    #########

    #################
    # NA close file #
    #################

    def test_input_of_na_status_file__close_file(self):
        manager_app = DataManagerApp.setup()

        # Create in _input dir - a NA file
        DataManagerApp.create_input_dir_file_na1()

        # Manager moves it to the _report dir
        manager_app.accept_new_reports()
        assert DataManagerApp.exists_report_dir_file_na1()

        # Create "close file" for na - now na should be removed
        DataManagerApp.create_input_dir_close_na_file1()
        assert DataManagerApp.exists_input_dir_close_file_na1()

        # Remove na file - as we now have a "close" file for it
        manager_app.remove_nas_requested_delete()
        assert not DataManagerApp.exists_report_dir_file_na1()
        assert not DataManagerApp.exists_input_dir_close_file_na1()

        DataManagerApp.clean_files()

    ###################
    # OKAY close file #
    ###################

    def test_input_of_okay_status_file__close_file(self):
        manager_app = DataManagerApp.setup()

        # Create in _input dir - an OKAY file
        DataManagerApp.create_input_dir_file_okay1()

        # Manager moves it to the _report dir
        manager_app.accept_new_reports()
        assert DataManagerApp.exists_report_dir_file_okay1()

        # Create "close file" for okay - now okay should be removed
        DataManagerApp.create_input_dir_close_okay_file1()
        assert DataManagerApp.exists_input_dir_close_file_okay1()

        # Remove okay file - as we now have a "close" file for it
        manager_app.remove_okays_requested_delete()
        assert not DataManagerApp.exists_report_dir_file_okay1()
        assert not DataManagerApp.exists_input_dir_close_file_okay1()

        DataManagerApp.clean_files()

    ###################
    # WARN close file #
    ###################

    def test_input_of_warn_status_file__close_file(self):
        manager_app = DataManagerApp.setup()

        # Create in _input dir - a WARN file
        DataManagerApp.create_input_dir_file_warn1()

        # Manager moves it to the _warn dir
        manager_app.accept_new_reports()
        assert DataManagerApp.exists_warn_dir_file_warn1()

        # No "close file" yet for warn - so warn not removed
        manager_app.remove_expired_okay_and_na_reports()
        assert DataManagerApp.exists_warn_dir_file_warn1()

        # Create "close file" for warn - now warn should be removed
        DataManagerApp.create_input_dir_close_warn_file1()
        assert DataManagerApp.exists_input_dir_close_file_warn1()

        # Remove warn file - as we now have a "close" file for it
        manager_app.remove_warns_requested_delete()
        assert not DataManagerApp.exists_warn_dir_file_warn1()
        assert not DataManagerApp.exists_input_dir_close_file_warn1()

        DataManagerApp.clean_files()

    ####################
    # ALERT close file #
    ####################

    def test_input_of_alert_status_file(self):
        manager_app = DataManagerApp.setup()

        # Create in _input dir - an ALRT file
        DataManagerApp.create_input_dir_file_alert1()

        # Manager moves it to the _alert dir
        manager_app.accept_new_reports()
        assert DataManagerApp.exists_alert_dir_file_alert1()

        # No "close file" yet for alert - so alert not removed
        manager_app.remove_expired_okay_and_na_reports()
        assert DataManagerApp.exists_alert_dir_file_alert1()

        # Create "close file" for alert - now alert should be removed
        DataManagerApp.create_input_dir_close_alert_file1()
        assert DataManagerApp.exists_input_dir_close_file_alert1()

        # Remove alert file - as we now have a "close" file for it
        manager_app.remove_alerts_requested_delete()
        assert not DataManagerApp.exists_alert_dir_file_alert1()
        assert not DataManagerApp.exists_input_dir_close_file_alert1()

        DataManagerApp.clean_files()
