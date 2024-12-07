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
    echo "  1. Local install"
    echo "  2. Dist build"
    echo ""
    echo "  3. Exit"
    echo ""
}

option_1() {
    current_dir=$(pwd)
    cd ..
    source ./venv/bin/activate
    clear
    pip uninstall -y montty
    pip install -e .
    pip list
    pip install -e .[dev]
    cd "$current_dir" || exit
}

option_2() {
    current_dir=$(pwd)
    cd ..
    source ./venv/bin/activate
    clear
    rm -f ./*.whl
    rm -rf src/montty.egg-info
    rm -rf build
    rm -rf dist
    python -m build --sdist
    python -m build --wheel
}

clear

# Main loop
while true; do
    display_menu
    read -r -p "Please enter your choice (1-3): " choice

    case $choice in
        1)
            option_1
            ;;
        2)
            option_2
            ;;
        3)
            echo "Exiting the program."
            break
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
done

