#!/bin/bash

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

# Function to display the menu
display_menu() {
    echo ".---------------------------------------------."
    echo "| Menu                                        | "
    echo "'---------------------------------------------'"
    echo "  1. Static analysis"
    echo "  2. Unit tests"
    echo "  3. Security scan"
    echo "  4. Shellcheck CHECKS bash scripts"
    echo "  5. Unit test CHECKS bash scripts"
    echo "  6. Directory scan"
    echo "  7. What is git ignored"
    echo ""
    echo "  8. Exit"
    echo ""
}

option_1() {
    ./RUN_SCRIPTS/run_static_analysis.sh
}

option_2() {
    ./RUN_SCRIPTS/run_unit_tests.sh
}

option_3() {
    ./RUN_SCRIPTS/run_sec.sh
}

option_4() {
    ./RUN_SCRIPTS/run_shellcheck.sh
}

option_5() {
    ./RUN_SCRIPTS/run_mtycmd_test.sh  
}

option_6() {
    ./RUN_SCRIPTS/run_dir_scan.sh  
}

option_7() {
    ./RUN_SCRIPTS/run_check_git_ignored.sh
}

clear

# Main loop
while true; do
    display_menu
    read -p "Please enter your choice (1-8): " choice

    case $choice in
        1)
            option_1
            ;;
        2)
            option_2
            ;;
        3)
            option_3
            ;;
        4)
            option_4
            ;;
        5)
            option_5
            ;;
        6)
            option_6
            ;;
        7)
            option_7
            ;;
        8)
            echo "Exiting the program."
            break
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
done

