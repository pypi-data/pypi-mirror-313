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

import os
import sys
import pathlib


class InstallDir:
    def __init__(self, path):
        self._path = path

    def get_path(self):
        return self._path

    @classmethod
    def _in_venv(cls):
        """ 
        sys.base_prefix will hold the path to the Python installation 
        directory used to create the virtual environment.

        sys.prefix will point to the Python installation directory of our 
        virtual environment in case we are using one. 

            If not using a virtual environment, will be the same as 
            sys.base_prefix.
        """
        return (hasattr(sys, 'real_prefix') or
                (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

    @classmethod
    def create_instance(cls):
        if not cls._in_venv():
            raise Exception(
                "Not in Python venv virtual environment")  # pragma: no cover
        # Strip off the virtual env (venv) name, which is the last part of the
        # path, returned by sys.prefix (if we ar ein a virtual environment,
        # which is checked above
        venv_path = os.path.dirname(sys.prefix)
        path_venv_removed = pathlib.Path(venv_path)
        return InstallDir(str(path_venv_removed))
