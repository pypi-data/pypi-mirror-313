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

import pytest
from montty.report.subject import Subject
from montty.report.header import Header


@pytest.fixture
def fixture_test_header_status_na():
    subject = Subject()
    subject.set_hostname("test_host")
    subject.set_ip("192.0.2.0")
    subject.set_status_na()
    subject.set_at_now()
    return Header(subject)


@pytest.fixture
def fixture_test_header_status_okay():
    subject = Subject()
    subject.set_hostname("test_host")
    subject.set_ip("192.0.2.0")
    subject.set_status_okay()
    subject.set_at_now()
    return Header(subject)


@pytest.fixture
def fixture_test_header_status_warn():
    subject = Subject()
    subject.set_hostname("test_host")
    subject.set_ip("192.0.2.0")
    subject.set_status_warn()
    subject.set_at_now()
    return Header(subject)


@pytest.fixture
def fixture_test_header_status_alert():
    subject = Subject()
    subject.set_hostname("test_host")
    subject.set_ip("192.0.2.0")
    subject.set_status_alert()
    subject.set_at_now()
    return Header(subject)


@pytest.fixture
def fixture_body_text_25():
    text = \
        "     head  1               (ALERT)                                                              \n" + \
        "     head  2               (WARN)                                                               \n" + \
        "     head  3               (OKAY)                                                               \n" + \
        "     head  4               (NA)                                                                 \n" + \
        "     line  5 ----- ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ -------\n" + \
        "     line  6 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line  7 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line  8 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line  9 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 10 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 11 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 12 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 13 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 14 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 15 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 16 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 17 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 18 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 19 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 20 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 21 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 22 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 23 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 24 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 25 line   line   line   line   line   line   line   line   line   line   line   line -\n"
    return text


@pytest.fixture
def fixture_body_text_50():
    text = \
        "head  1               (ALERT)                                                              \n" + \
        "head  2               (WARN)                                                               \n" + \
        "head  3               (OKAY)                                                               \n" + \
        "head  4               (NA)                                                                 \n" + \
        "SUMMARY 5                                                                                  \n" + \
        "line  6 ----- ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ -------\n" + \
        "     line  7 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line  8 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line  9 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 10 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 11 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 12 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 13 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 14 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 15 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 16 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 18 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 19 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 20 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 21 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 22 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 23 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 24 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 25 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 26 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 27 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 28 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 29 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 30 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 31 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 32 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 33 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 34 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 35 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 36 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 37 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 38 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 39 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 40 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 41 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 42 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 43 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 44 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 45 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 46 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 47 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 48 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 49 line   line   line   line   line   line   line   line   line   line   line   line -\n" + \
        "     line 50 line   line   line   line   line   line   line   line   line   line   line   line -\n"
    return text
