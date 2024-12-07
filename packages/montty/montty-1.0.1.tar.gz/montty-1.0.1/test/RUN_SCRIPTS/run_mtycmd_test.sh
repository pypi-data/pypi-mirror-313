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

test_title () {
  printf "\n%-70s" "$1"
}

test_exit_code () {
  output=$1
  exit_code=$2
  expected_exit_code=$3
  echo ""
  echo "output             -->>  $output"
  echo "exit_code          -->>  $exit_code"
  echo "expected_exit_code -->>  $expected_exit_code"

  if [[ $exit_code -eq $expected_exit_code ]];
   then
      echo "    pass"
   else
      echo "    FAIL"
      exit 1
  fi
}

echo ""
echo "-------------------------------S t a r t------------------------------" 
echo ""

clear

# Cd into where the bash scripts to be tested should be

cd ../CHECKS/BASH_SCRIPTS/mty_util || exit

echo ""
echo ".--------------------------------------------------------------------."
echo "| host_eq                                                            |" 
echo "'--------------------------------------------------------------------'"
echo ""

test_title "T1a: Hostname matches"
output=$(./mtyhost.sh host_eq "$(hostname)");exit_code=$?
test_exit_code "$output" $exit_code 0

test_title "T1b: Hostname NOT matches"
output=$(./mtyhost.sh host_eq bad);exit_code=$?
test_exit_code "$output" $exit_code 254

echo ""
echo ".--------------------------------------------------------------------."
echo "| host_in                                                            |" 
echo "'--------------------------------------------------------------------'"
echo ""

# Single hostname

test_title "T2a: Single hostname, no trailing \\n"
output=$(./mtyhost.sh host_in "$(hostname)");exit_code=$?
test_exit_code "$output" $exit_code 0

test_title "T2b: NOT found in single hostname, no trailing \\n"
output=$(./mtyhost.sh host_in bad);exit_code=$?
test_exit_code "$output" $exit_code 254

test_title "T3a: Found in single hostname, with trailing \\n"
output=$(./mtyhost.sh host_in "$(hostname)\n");exit_code=$?
test_exit_code "$output" $exit_code 0

test_title "T3b: NOT found in single hostname, with trailing \\n"
output=$(./mtyhost.sh host_in "bad\n");exit_code=$?
test_exit_code "$output" $exit_code 254

# Double hostnames

test_title "T4a: Found in double hostnames, with current first"
output=$(./mtyhost.sh host_in "$(hostname)\nbad\n");exit_code=$?
test_exit_code "$output" $exit_code 0

test_title "T4b: NOT found in double hostnames"
output=$(./mtyhost.sh host_in "bad1\nbad2\n");exit_code=$?
test_exit_code "$output" $exit_code 254

test_title "T5a: Found in double hostnames, with current second"
output=$(./mtyhost.sh host_in "bad\n$(hostname)\n");exit_code=$?
test_exit_code "$output" $exit_code 0

test_title "T5b: Found in double hostnames, with current second and no trailing \n"
output=$(./mtyhost.sh host_in "bad\n$(hostname)");exit_code=$?
test_exit_code "$output" $exit_code 0

echo ""
echo ".--------------------------------------------------------------------."
echo "| host_not_in                                                        |" 
echo "'--------------------------------------------------------------------'"
echo ""

test_title "T6a: Not found in single hostname, no trailing \n"
output=$(./mtyhost.sh host_not_in bad);exit_code=$?
test_exit_code "$output" $exit_code 0

test_title "T6b: FOUND in single hostname, no trailing \\n"
output=$(./mtyhost.sh host_not_in "$(hostname)");exit_code=$?
test_exit_code "$output" $exit_code 254

echo ""
echo ".--------------------------------------------------------------------."
echo "| distro_eq                                                          |" 
echo "'--------------------------------------------------------------------'"
echo ""

test_title "T7a: Match for debian distro"
output=$(./mtyhost.sh distro_eq debian);exit_code=$?
test_exit_code "$output" $exit_code 0

test_title "T7b: NOT match for debian distro"
output=$(./mtyhost.sh distro_eq rhel);exit_code=$?
test_exit_code "$output" $exit_code 254

echo ""
echo ".----------------------------------------------------------------------."
echo "| distro_in                                                            |" 
echo "'----------------------------------------------------------------------'"
echo ""
. /etc/os-release
this_distro=$ID

# Single distro

test_title "T8a: Single distro, no trailing \\n"
output=$(./mtyhost.sh distro_in "${this_distro}");exit_code=$?
test_exit_code "$output" $exit_code 0

test_title "T8b: NOT found in distro, no trailing \\n"
output=$(./mtyhost.sh distro_in bad);exit_code=$?
test_exit_code "$output" $exit_code 254

test_title "T8a: Found in single distro, with trailing \\n"
output=$(./mtyhost.sh distro_in "${this_distro}\n");exit_code=$?
test_exit_code "$output" $exit_code 0

test_title "T8b: NOT found in single distro, with trailing \\n"
output=$(./mtyhost.sh distro_in "bad\n");exit_code=$?
test_exit_code "$output" $exit_code 254

# Double distros

test_title "T8a: Found in double distros, with current first"
output=$(./mtyhost.sh distro_in "${this_distro}\nbad\n");exit_code=$?
test_exit_code "$output" $exit_code 0

test_title "T8b: NOT found in double distros"
output=$(./mtyhost.sh distro_in "bad1\nbad2\n");exit_code=$?
test_exit_code "$output" $exit_code 254

test_title "T8a: Found in double dsitros, with current second"
output=$(./mtyhost.sh distro_in "bad\n${this_distro}\n");exit_code=$?
test_exit_code "$output" $exit_code 0

test_title "T8b: Found in double distrox, with current second and no trailing \n"
output=$(./mtyhost.sh distro_in "bad\n${this_distro}");exit_code=$?
test_exit_code "$output" $exit_code 0

echo ""
echo "---------------------------------E n d--------------------------------" 
echo ""
