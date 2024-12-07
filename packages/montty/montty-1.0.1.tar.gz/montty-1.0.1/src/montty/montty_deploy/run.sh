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



# ##################################################################### #
#  Function: usage
#  Args: None
#  Vars: None
# ##################################################################### #

function usage() {

cat << HEREDOC

Usage: 
  ./run.sh [-h|--help]

      Show this help message and exit


  ./run.sh [mon|monitor]

      Run the MonTTY monitor app


  ./run.sh [man|manager]

      Run the MonTTY manager app

      Should be in MonTTY user's crontab


  ./run.sh [chk|checker] "" SCP_USER SCP_SERVER SCP_DEST_DIR
  ./run.sh [chk|checker] "FILTER TAG(S)" SCP_USER SCP_SERVER SCP_DEST_DIR

      Run the MonTTY checker app  "remotely" on hosts to be checked

      This will run the check files, and scp the corresponding check report to the
      MonTTY server 

      To do this, you need to provide the scp user, server and the scp destination 
      directory 

      This command should be in MonTTY user's crontab


  ./run.sh [local_chk|local_checker] ""
  ./run.sh [local_chk|local_checker] "FILTER TAG(S)"

      Run the MonTTY checker app "locally" on the MonTTY server

      Typically used for testing, or for running the MonTTY checker app additionally -
      "locally" on the MonTTY server

      If not used for testing, then the command should be in MonTTY user's crontab

HEREDOC
}  



# ##################################################################### #
#  Function run_monitor
#  Args: None
#  Vars: None
# ##################################################################### #

function run_monitor() {

  # --------------------------------------------------- #
  # Run MonTTY Monitor app                              #
  # --------------------------------------------------- #

  montty-monitor

  # --------------------------------------------------- #
  # Handle pontential crash or user ^C                  #
  #                                                     #
  # Gives possibility of ncurses not getting cleaned    #
  # up, leaving the terminal in a "bad state" for       #
  # the user                                            #
  #                                                     #
  # Proactively clean with "stty sane/echo" to force    #
  # clean reset                                         #
  # --------------------------------------------------- #

  stty sane
  stty sane
  stty echo
}


# ##################################################################### #
#  Function run_manager
#  Args: None
#  Vars: None
# ##################################################################### #

function run_manager() {

  # --------------------------------------------------- #
  # Run MonTTY Manager app                              #
  # --------------------------------------------------- #

  montty-manager
}



# ##################################################################### #
#  Function: run_checker(
#  Args: None
#  Vars: TAGS, INPUT_FILES_DIR,
# ##################################################################### #

function run_checker() {  
  
  # --------------------------------------------------- #
  # Number arguments to script must be 5 for this app   #
  # --------------------------------------------------- #

  if [ $NUMBER_SCRIPT_ARGS != 5 ] ; then 
    echo "ERROR: This app requires 2 arguments" >&2 
    usage
    exit 1 
  fi

  # --------------------------------------------------- #
  # Run MonTTY Checker app, and scp the generated       #
  # check report to the MonTTY server                   #
  # --------------------------------------------------- #

  if montty-checker "${TAGS}"; then
      # As Checker app was succcessfil then transfer check 
      # report files to the server using 'scp' to the
      # MonTTY server

      # Example:
      #
      # scp ${INPUT_FILES_DIR}/*.mty mtyuser@192.0.2.0:~/montty/REPORTS/_input

      echo "scp ${INPUT_FILES_DIR}/*.mty ${SCP_USER}@${SCP_SERVER}:${SCP_FILES_DIR}"

      scp "${INPUT_FILES_DIR}"/*.mty "${SCP_USER}@${SCP_SERVER}:${SCP_FILES_DIR}"

      # Remove the transferred file(s)
      #
      rm "${INPUT_FILES_DIR}"/*.mty
      echo ""
  else
      echo montty-checker failed
  fi
}


# ##################################################################### #
#  Function: run_local_checkerd
#  Args: None
#  Vars: TAGS, INPUT_FILES_DIR,
# ##################################################################### #

function run_local_checker() {

  # --------------------------------------------------- #
  # Number arguments to script must be 2 for this app   #
  # --------------------------------------------------- #

  if [ $NUMBER_SCRIPT_ARGS != 2 ] ; then 
    echo "" >&2
    echo "ERROR: The MonTTY [local_chk|local_checker] app selection, requires an argument" >&2 
    echo "           - The 'filter tags' value:" >&2 
    echo "                 \"\"                    For no filter tags" >&2
    echo "" >&2
    echo "" >&2
    echo "                 \"<FILTTER TAG(S)>\"    To specify filter tags" >&2
    echo "" >&2
    echo "                     Example: \"bash_check python_check collect_check\" " >&2
    echo "" >&2
    #usage
    exit 1 
  fi


  # --------------------------------------------------- #
  # Run MonTTY Checker app                              #
  # --------------------------------------------------- #

  montty-checker "${TAGS}"
}


# ##################################################################### #
# MAIN                                                                  #
# ##################################################################### #

# ----------------------------------------------------- #
# Initialize variables from script call arguments       #
# ----------------------------------------------------- #

# Check we have at least one argument - the app

if [ $# == 0 ] ; then 
  echo "ERROR: Must have at least one arg - the MonTTY app to be run" >&2 
  usage
  exit 1
fi

NUMBER_SCRIPT_ARGS=$#
APP=$1
TAGS=$2
SCP_USER=$3
SCP_SERVER=$4
SCP_FILES_DIR=$5


# ----------------------------------------------------- #
# Get the directory this script is located in           #
# ----------------------------------------------------- #

# Set THIS_SCRIPT_DIR to the absolute path, of the directory 
# where the sccript is located
#
#     dirname "$SOURCE": 
#         This gets the directory part of the variable 
#         SOURCE, which should contain the path to the 
#         script. 
#
#
#     cd -P "$( dirname "$SOURCE" )": 
#         This changes the current directory to the one obtained 
#         from dirname. 
#
#         The -P option tells cd to follow symbolic links and 
#         resolve the actual directory path.
#
#
#     >/dev/null 2>&1: 
#         This part redirects both standard output and standard 
#         error to /dev/null, effectively silencing any output or 
#         error messages from the cd command.
#
#
#     && pwd: 
#         If the cd command is successful, pwd is executed, which 
#         prints the current directory (now the directory of the 
#         script).

SOURCE=${BASH_SOURCE[0]}
THIS_SCRIPT_DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )


# ----------------------------------------------------- #
# Set the REPORTS/_input files directory full path,     #
# used by MonTTY Checker app                            #
# ----------------------------------------------------- #

INPUT_FILES_DIR=${THIS_SCRIPT_DIR}/REPORTS/_input


# ----------------------------------------------------- #
# Activate the Python virtual environment               #
# ----------------------------------------------------- #

source "${THIS_SCRIPT_DIR}"/venv/bin/activate


# ----------------------------------------------------- #
# Select the particular MonTTY app functionality        #
# ----------------------------------------------------- #

# Select app to run

case "$APP" in
    -h        | --help        ) usage; exit; ;;
    mon       | monitor       ) run_monitor; exit; ;;
    man       | manager       ) run_manager; exit; ;;
    chk       | checker       ) run_checker; exit; ;;
    local_chk | local_checker ) run_local_checker; exit; ;;
    *                         ) echo ""; echo "**** Command $1 not recognized"; usage; exit;;
esac

