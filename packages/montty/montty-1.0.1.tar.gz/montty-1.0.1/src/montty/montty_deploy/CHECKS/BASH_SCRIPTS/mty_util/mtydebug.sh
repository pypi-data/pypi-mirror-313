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

status_alert() {
  echo "Exit status code is > 0 and < 253, this becomes status ALERT"; exit 1
}

status_warn() {
  echo "Exit status code is 255, this becomes status WARN"; exit 255
}

status_okay() {
  echo "Exit status code is 0, this becomes status OKAY"; exit 0
}

status_na() {
  echo "Exit status code is 254, this becomes status NA"; exit 254
}

echo_call() {
  echo "Arguments received in the function:"
  for arg in "$@"; do
      echo "  $arg"
  done
  
  exit 0
}

######## 
# MAIN #
######## 

CMD=$1

case "$CMD" in
    status_alert)
        status_alert 
        ;;
    status_warn)
        status_warn
        ;;
    status_okay)
        status_okay
        ;;
    status_na)
        status_na
        ;;
    echo_call)
        echo_call "$@"
        ;;
    *)
        echo "Unsupported command $CMD args $*"
        exit 1
        ;;
esac
