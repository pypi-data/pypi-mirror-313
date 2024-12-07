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
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR,
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


service_installed(){
    local service_name=$1
    if ! systemctl status "$service_name" &>/dev/null; then
        echo "Service $service_name is NOT installed"
        return 2
    else
        echo "Service $service_name IS installed"
        return 0
    fi
}


service_enabled(){
    local service_name=$1
    if ! systemctl is-enabled "$service_name" &>/dev/null; then
        echo "Service $service_name is NOT enaled"
        return 3
    else
        echo "Service $service_name IS enabled"
        return 0
    fi
}


service_active(){
    local service_name=$1
    if ! systemctl is-active "$service_name" &>/dev/null; then
        echo "Service $service_name is NOT active"
        return 4
    else
        echo "Service $service_name IS active"
        return 0
    fi
}


#------#
# MAIN #
#------#

# Check if the number of arguments is not equal to 1
if [ $# -ne 2 ]; then
    echo "Error: Expected 2 argumentsi:  'command service_name', but got $# -> '$*'"
    exit 1
fi

command=$1
service_name=$2

case "$command" in
    installed)
        service_installed "$service_name";
        exit $?;
        ;;
    enabled)
        service_enabled "$service_name";
        exit $?;
        ;;
    active)
        service_active "$service_name";
        exit $?;
        ;;
    installed_enabled_active)
        service_installed "$service_name" && service_enabled "$service_name" && service_active "$service_name"
        exit $?
        ;;
    *)
        echo "Unsupported command $CMD"
        exit 1
        ;;
esac
