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

import csv


class LsofRowValue:
    ''' Represent lsof row value - which is a row of output from the lsof command

    The rows from the output of the lsof command, are also stored in a CSV data file
    These values represent the "allowed" valuesi, from the lsof command output

    The format for a row is:
        COMMAND,USER,IP_TYPE,NODE
        dhclient,root,IPv4,UDP
        avahi-dae,avahi,IPv4,UDP
        avahi-dae,avahi,IPv6,UDP '''

    def __init__(self, command, user, ip_type, node):
        self._command = command
        self._user = user
        self._ip_type = ip_type
        self._node = node

    def get_command(self):
        return self._command

    def get_user(self):
        return self._user

    def get_ip_type(self):
        return self._ip_type

    def get_node(self):
        return self._node

    # Is equal to another LsofRowValue instance
    # Self not available in Python 3.9, needs 3.11
    #   def __eq__(self, other_value: Self):
    def __eq__(self, other_value):
        if self._command == other_value.get_command() and \
           self._user == other_value.get_user() and \
           self._ip_type == other_value.get_ip_type() and \
           self._node == other_value.get_node():
            return True
        return False

    def __str__(self):
        return f"{self._command:>12}, {self._user:>12}, {self._ip_type:>12}, {self._node:>12}\n"

    @classmethod
    def str_header(cls):
        return f'{"COMMAND":>12}, {"USER":>12}, {"IP_TYPE":>12}, {"NODE":>12}\n'


class AllowedLsofRowValues:
    def __init__(self):
        self._lsof_values = []
        self._mismatches = ''

    def read_values(self, data_file_full_name: str):
        with open(data_file_full_name, mode='r', newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                lsof_value = LsofRowValue(
                    row['COMMAND'], row['USER'], row['IP_TYPE'], row['NODE'])
                self._lsof_values.append(lsof_value)

    def __str__(self):
        string_value = LsofRowValue.str_header()

        for lsof_value in self._lsof_values:
            string_value += str(lsof_value)
        return string_value

    def __iter__(self):
        return iter(self._lsof_values)

    def contains_value(self, actual_lsof_value: LsofRowValue):
        contains = False
        for allowed_lsof_value in self._lsof_values:
            if actual_lsof_value == allowed_lsof_value:
                contains = True
                break
        return contains

    def contains_all_values(self, actual_lsof_values):
        contains_all = True
        for actual_lsof_value in actual_lsof_values:
            if not self.contains_value(actual_lsof_value):
                contains_all = False
                self._mismatches += str(actual_lsof_value)
                # break
        return contains_all

    def get_mismatches(self):
        if self._mismatches:
            value = LsofRowValue.str_header()
            value += self._mismatches
            return value
        return self._mismatches


class ActualLsofRowValues:
    def __init__(self, command_output):
        self._command_output = command_output
        self._lsof_values = []

    def parse(self):
        # Split the data into lines
        lines = self._command_output.strip().split('\n')

        # Extract header and rows
        header = lines[0].split()
        command_index = header.index('COMMAND')
        user_index = header.index('USER')
        ip_type_index = header.index('TYPE')
        node_index = header.index('NODE')

        # Extract specific columns
        rows = [line.split() for line in lines[1:]]
        for row in rows:
            command = row[command_index]
            user = row[user_index]
            ip_type = row[ip_type_index]
            node = row[node_index]
            lsof_value = LsofRowValue(command, user, ip_type, node)
            self._lsof_values.append(lsof_value)

    def __str__(self):
        string = "COMMAND, USER, IP_TYPE, NODE\n"
        string = f'{"COMMAND":>12}, {"USER":>12}, {"IP_TYPE":>12}, {"NODE":>12}\n'
        for lsof_value in self._lsof_values:
            string += str(lsof_value)
        return string

    def __iter__(self):
        return iter(self._lsof_values)
