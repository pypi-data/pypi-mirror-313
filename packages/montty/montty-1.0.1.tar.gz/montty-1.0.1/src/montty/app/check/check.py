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

from abc import ABC, abstractmethod
from montty.app.status import Status
from montty.app.check.check_header import CheckHeader


class Check(ABC):
    '''Represents all checks

    A check at its core, is a status and body text representing the output of 
    the check, whether it passes or fails '''

    def get_output(self) -> str:
        '''Output check result

        This is the header and status as the first line

        Then, the check's body text, which is the output from the check'''

        # Build check header for the output's "header line"
        header = self.get_header()
        output = str(header)

        # Now add the check's body or "results" if there are any
        output += str(self.get_body()).rstrip()

        # Make sure the last character of the body is a \n, so we can standardize
        # the output formatting
        if output and output[-1] != '\n':
            output += "\n"
        return output

    # Allows us to sort checks by their headers

    def __lt__(self, other):
        return self.get_header().get_title() < other.get_header().get_title()

    def __gt__(self, other):
        return self.get_header().get_title() > other.get_header().get_title()

    def __eq__(self, other):
        return self.get_header().get_title() == other.get_header().get_title()

    # For sub classes to implement

    @abstractmethod
    # pragma: no cover
    def run(self) -> None:
        raise Exception("You must implement this method")

    @abstractmethod
    # pragma: no cover
    def get_status(self) -> Status:
        raise Exception("You must implement this method")

    @abstractmethod
    # pragma: no cover
    def get_header(self) -> CheckHeader:
        raise Exception("You must implement this method")

    @abstractmethod
    # pragma: no cover
    def get_body(self):
        raise Exception("You must implement this method")
