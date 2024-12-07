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

class ConfigValues:
    LOGO = 'MonTTY'

    ################
    # CHECK REPORT #
    ################

    # Time-To-Live (TTL) stamped in all check report files, not actually used
    # with ALERT status files
    CHECK_REPORT_FILE_TTL_SECS = 300

    ################
    # LICENSE TEXT #
    ################

    LICENSE_TEXT = [
        "MIT License",
        "",
        "Copyright (c) 2024 Gwyn Davies",
        "",
        "Permission is hereby granted, free of charge, to any person obtaining a copy",
        "of this software and associated documentation files (the \"Software\"), to deal",
        "in the Software without restriction, including without limitation the rights",
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell",
        "copies of the Software, and to permit persons to whom the Software is",
        "furnished to do so, subject to the following conditions:",
        "",
        "The above copyright notice and this permission notice shall be included in all",
        "copies or substantial portions of the Software.",
        "",
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR,",
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,",
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE",
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER",
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,",
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE",
        "SOFTWARE.",
    ]

    #####################
    # SCREEN / TERMINAL #
    #####################

    TERMINAL_MIN_WIDTH = 95
    TERMINAL_MIN_HEIGHT = 25

    #######################
    # META INFO DIRECTORY #
    #######################

    META_INFO_KEY = 'montty'

    ###################
    # CHECKS GGENERAL #
    ###################

    CHECK_MAX_HEADER_TITLE_LENGTH = 65
    CHECK_MIN_LEVEL = 0
    CHECK_MAX_LEVEL = 5

    ####################
    # CHECKS Directory #
    ####################

    CHECKS_DIR_NAME = 'CHECKS'
    CHECKS_DIR_PYTHON_LIBS_DIR_NAME = 'PYTHON_LIBS'
    CHECKS_DIR_BASH_SCRIPTS_DIR_NAME = 'BASH_SCRIPTS'
    CHECKS_DIR_DATA_FILES_DIR_NAME = 'DATA_FILES'

    # Glob pattern for 'One-Line' check files - chk*.oln Chk*.oln CHK*.oln ... etc.
    GLOB_PATTERN_ONE_LINE_CHECK_FILES = '[c|C][h|H][k|K]*.oln'

    # Glob pattern for 'Python' check files - chk*.py Chk*.py CHK*.py ... etc.
    GLOB_PATTERN_PYTHON_CHECK_FILES = '[c|C][h|H][k|K]*.py'

    #####################
    # REPORTS DIRECTORY #
    #####################

    REPORTS_DIR_NAME = 'REPORTS'
    REPORTS_DIR_INPUT_DIR_NAME = '_input'
    REPORTS_DIR_REPORT_DIR_NAME = '_report'
    REPORTS_DIR_WARN_DIR_NAME = '_warn'
    REPORTS_DIR_ALERT_DIR_NAME = '_alert'

    #########
    # FILES #
    #########

    FILE_ENCODING = 'utf-8'
    CHECK_REPORT_FILE_EXTENSION = '.mty'
    CHECK_CLOSE_MESSAGE_FILE_EXTENSION = '.close'
    CHECK_OLN_FILE_COMMENT_CHAR = '#'
    CHECK_OLN_FILE_LINE_SEPARATOR = '#mty#'

    ############
    # MESSAGES #
    ############

    CHECK_REPORT_CLOSE_MESSAGE = 'close'

    ##################
    # LINUX COMMANDS #
    ##################

    # Base on Linux standard interpretation, but take 255 to be used for WARN
    # 0      OKAY
    # 255    WARN
    # 1..254 ALERT
    LINUX_COMMAND_EXIT_STATUS_CODE_OKAY = 0
    LINUX_COMMAND_EXIT_STATUS_CODE_NA = 254
    LINUX_COMMAND_EXIT_STATUS_CODE_WARN = 255
    LINUX_COMMAND_EXIT_STATUS_CODE_ALERT_MIN = 1
    LINUX_COMMAND_EXIT_STATUS_CODE_ALERT_MAX = 253

    ################
    # BASH SCRIPTS #
    ################

    BASH_SCRIPT_NAME_MAX_LENGTH = 64
    BASH_SCRIPT_ARGUMENT_MAX_LENGTH = 128

    ########
    # APPS #
    ########

    CHECK_APP_MAX_TAGS_PARAM_LEN = 256
