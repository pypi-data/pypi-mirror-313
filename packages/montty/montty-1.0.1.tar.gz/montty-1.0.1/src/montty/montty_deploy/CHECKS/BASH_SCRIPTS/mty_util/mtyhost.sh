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

#-----------------------------------------------#
# Linux Distribution [debian, ubuntu, rhel ...] #
#-----------------------------------------------#

detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    else
        echo "unknown"
    fi
}

distro_eq() {
    current_distro=$(detect_distro)
    local to_distro=$1
    echo "-> Test distro_eq ${to_distro} = $current_distro"
    [ "${current_distro}" = "${to_distro}" ] && exit 0 || exit 254
}

distro_not_eq() {
    current_distro=$(detect_distro)
    local to_distro=$1
    echo "-> Test distro_not_eq ${to_distro} = $current_distro"
    [ "${current_distro}" != "${to_distro}" ] && exit 0 || exit 254
}

# distro_in <to distros>
#   to_distros ... list of distros to check against, separate names by \n
#     distro1
#     distro1\n
#     distro1\ndistro2\n
#     distro1\ndistro2
distro_in() {
    local to_distros=$1
    echo "-> Test distro_in $to_distros"
    detect_distro | /usr/bin/grep -q -w -F -f <(echo -e "${to_distros}") && exit 0 || exit 254
}

# distro_not_in <to distros>
#   to_distros ... list of distros to check against, separate names by \n
#     distro1
#     distro1\n
#     distro1\ndistro2\n
#     distro1\ndistro2
distro_not_in() {
    local to_distros=$1
    echo "-> Test distro_not_in $to_distros"
    detect_distro | /usr/bin/grep -q -w -F -f <(echo -e "${to_distros}") && exit 254 || exit 0
}

#----------#
# Hostname #
#----------#

host_eq() {
    local to_hostname=$1
    echo "-> Test host_eq ${to_hostname}"
    [ "$(hostname)" = "${to_hostname}" ] && exit 0 || exit 254
}

# host_not_eq <to hostname>
host_not_eq() {
    local to_hostname=$1
    echo "-> Test host_not_eq ${to_hostname}"
    [ "$(hostname)" != "${to_hostname}" ] && exit 0 || exit 254
}

# host_in <to hostnames>
#   to_hostnames ... list of hostnames to check against, separate names by \n
#     hostname1
#     hostname1\n
#     hostname1\nhostname2\n
#     hostname1\nhostname2
host_in() {
    local to_hostnames=$1
    echo "-> Test host_in $to_hostnames"
    hostname | /usr/bin/grep -q -w -F -f <(echo -e "${to_hostnames}") && exit 0 || exit 254
}

# host_not_in <to hostnames>
#   to_hostnames ... list of hostnames to check against, separate names by \n
#     hostname1
#     hostname1\n
#     hostname1\nhostname2\n
#     hostname1\nhostname2
host_not_in() {
    local to_hostnames=$1
    echo "-> Test host_not_in $to_hostnames"
    hostname | /usr/bin/grep -q -w -F -f <(echo -e "${to_hostnames}") && exit 254 || exit 0
}

#------#
# MAIN #
#------#

CMD=$1
ARGS=$2

case "$CMD" in
    # Distro(s)
 
    distro_eq)
        distro_eq  "$ARGS" 
        ;;
    distro_not_eq)
        distro_not_eq  "$ARGS" 
        ;;

    distro_in)
        distro_in  "$ARGS" 
        ;;
    distro_not_in)
        distro_not_in  "$ARGS" 
        ;;

    # Hostname(s)
 
    host_eq)
        host_eq  "$ARGS" 
        ;;
    host_not_eq)
        host_not_eq  "$ARGS" 
        ;;

    host_in)
        host_in  "$ARGS" 
        ;;
    host_not_in)
        host_not_in  "$ARGS" 
        ;;

    *)
        echo "Unsupported command $CMD"
        exit 1
        ;;
esac
