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

import ast
import re
from montty.app.check.root_check import RootCheck
from montty.platform.config_values import ConfigValues


class ParsedClass:
    def __init__(self, module_name, class_name, base_class_names, method_names):
        self._module_name = module_name
        self._class_name = class_name
        self._base_class_names = base_class_names
        self._method_names = method_names

    def __str__(self):
        as_str = ""
        as_str += "\nmodule name:\n    " + self._module_name + '\n'
        as_str += "\nclass name:\n    " + self._class_name + '\n'
        as_str += "base class(es):\n   "
        for base_class_name in self._base_class_names:
            as_str += " " + base_class_name
        as_str += "\nmethod(s):\n   "
        for method_name in self._method_names:
            as_str += " " + method_name
        as_str += "\n"
        return as_str

    def get_module_name(self):
        return self._module_name

    def get_class_name(self):
        return self._class_name

    def get_base_class_names(self):
        return self._base_class_names

    def get_number_base_classes(self):
        return len(self._base_class_names)

    def get_method_names(self):
        return self._method_names

    def get_number_methods(self):
        return len(self._method_names)


class CheckFileParser:
    @classmethod
    def create_instance(cls, file_path_name):
        with open(file_path_name, "r", encoding=f"{ConfigValues.FILE_ENCODING}") as f:
            file_text = f.read()
            return CheckFileParser(file_path_name, file_text)

    def __init__(self, file_path_name: str, file_text: str):
        self._file_path_name = file_path_name
        self._module_name = self._extract_module_name()
        self._file_text = file_text

    def get_module_name(self):
        return self._module_name

    def _extract_module_name(self):
        p = re.compile(r"^.*\/(\w+)\.py")
        module = p.search(self._file_path_name)
        if module:
            module_name = module.group(1)
        else:
            raise Exception('Cannot extract filename')
        return module_name

    def parse(self):
        p = ast.parse(self._file_text)

        # get all classes from the given python file.
        classes = [c for c in ast.walk(p) if isinstance(c, ast.ClassDef)]

        classes_found = []
        for clazz in classes:
            method_names = [fun.name for fun in ast.walk(
                clazz) if isinstance(fun, ast.FunctionDef)]
            base_class_names = [base_class.id for base_class in clazz.bases]
            classes_found.append(ParsedClass(
                self.get_module_name(), clazz.name,  base_class_names, method_names))

        # Find candiates for the root check class
        #
        # There must be one class that:
        #     Inherits from RootCheck - tag class that indicates the 'root check' class
        #     Inherits from another class, that is descended from Check
        #
        potential_root_check_classes = []

        for class_found in classes_found:
            base_class_names = class_found.get_base_class_names()
            if len(base_class_names) >= 2:
                if RootCheck.__name__ in base_class_names:
                    potential_root_check_classes.append(class_found)

        # Check what was found - we must have ONE root check class

        # More than one match found -> we can only have 1 'root check'
        if len(potential_root_check_classes) > 1:
            potential_root_check_class_names = []
            for potential_class in potential_root_check_classes:
                potential_root_check_class_names.append(
                    potential_class.get_class_name())
            raise Exception(
                f"More than 1 root check class found, must be only one. Found {potential_root_check_class_names}")

        # No match found -> we must have a 'root checki
        if len(potential_root_check_classes) < 1:
            raise Exception(
                "No root check class found, must be one (and only one)")

        # Match found -> we found a class identified as the 'root check'
        return potential_root_check_classes[0]

    def dump(self):
        p = ast.parse(self._file_text)
        return ast.dump(p, indent=4)
