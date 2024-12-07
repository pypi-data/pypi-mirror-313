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
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

clear

pytest -s -vv --cov --cov-report term-missing ./

# IO
#pytest -s -vv --cov --cov-report term-missing ./io/file
#pytest -s -vv --cov --cov-report term-missing ./io/file/test_checks_dir.py
#pytest -s -vv --cov --cov-report term-missing ./io/file/test_check_tags_file.py
#pytest -s -vv --cov --cov-report term-missing ./io/file/test_file_util.py
#pytest -s -vv --cov --cov-report term-missing ./io/file/test_reports_dir.py

# App
#pytest -s -vv --cov --cov-report term-missing ./app/test_status.py

# Checker
#pytest -s -vv --cov --cov-report term-missing ./app/check/file/test_check_file_parser.py
#pytest -s -vv --cov --cov-report term-missing ./app/check/file/test_dynamic_import.py
#pytest -s -vv --cov --cov-report term-missing ./app/check/file/test_dynamic_instance.py
#pytest -s -vv --cov --cov-report term-missing ./app/check/test_bash_check.py

#pytest -s -vv --cov --cov-report term-missing ./app/check/test_check.py
#pytest -s -vv --cov --cov-report term-missing ./app/check/test_check_level.py
#pytest -s -vv --cov --cov-report term-missing ./app/check/test_check_header.py
#pytest -s -vv --cov --cov-report term-missing ./app/check/test_program_check.py
#pytest -s -vv --cov --cov-report term-missing ./app/check/test_collect_base_check.py

# Manager
#pytest -s -vv --cov --cov-report term-missing ./app/manager/test_manager_app.py

# Monitor - alert
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_alert
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_alert/test_monitor_app_init.py
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_alert/test_monitor_app_single.py
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_alert/test_monitor_app_double.py  
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_alert/test_monitor_app_delete.py

# Monitor - warn
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_warn
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_warn/test_monitor_app_init.py
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_warn/test_monitor_app_single.py
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_warn/test_monitor_app_double.py  
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_warn/test_monitor_app_delete.py

# Monitor - okay
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_okay
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_okay/test_monitor_app_init.py
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_okay/test_monitor_app_single.py
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_okay/test_monitor_app_double.py  
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_okay/test_monitor_app_delete.py

# Monitor - na 
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_na
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_na/test_monitor_app_init.py
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_na/test_monitor_app_single.py
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_na/test_monitor_app_double.py  
#pytest -s -vv --cov --cov-report term-missing ./app/monitor_na/test_monitor_app_delete.py

# Platform
#pytest -s -vv --cov --cov-report term-missing ./platform/test_platform_command.py
