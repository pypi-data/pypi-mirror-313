<!--
MIT License
 
Copyright (c) 2024 Gwyn Davies
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-->

## 1 - DISCLAIMERS

All trademarks, service marks, and product names mentioned in this document are the property of their respective owners

<br/>

**Always follow your organization's policies and procedures**, if there is a conflict between them, and any of the installation or other instructions for MonTTY

<br/>
<br/>
<br/>
<br/>

## 2 - OVERVIEW

All check files in MonTTY are Python scripts, that exist in MonTTY's *project directory* under **CHECKS** 

<br/>
<br/>

The file names for check files, must start with **chk** (they are lower-cased internally by MonTTY):

* They are stored in separate Python files, named as:
    * **chk{valid Linux filename chars}.py**
    * Example: **chk_001_bash_listening_ports_with_ss.py**

All the supporting files for checks go in sub-directories, under the CHECKS directory

<br/>
<br/>
<br/>
<br/>

## 3 - "CHECKS" DIRECTORY

```
    MonTTY project directory
        |
        |
        '---- CHECKS
                |
                | - Your check files go here ...
                |
                |
                |---- BASH_SCRIPTS
                |        |
                |        ' - Your bash script files for checks go here ...
                |
                |---- DATA_FILES
                |        |
                |        ' - Your data files for checks go here ...
                |
                '---- PYTHON_LIBS
                         |
                         ' - Your Python code used by checks can go here ...

```

<br/>
<br/>

### Example check files

MonTTY comes with some *example* check files:

| File name | Type | Sub-type | Other features | Checks |
| --------- | ---- | -------- | -------------- | ------ |
| chk_001_bash_listening_ports_with_ss.py | bash | None | None | Listening ports with ss command |
| chk_002_python_host_cpu.py | Python | None | None | Host cpu |
| chk_003_cla_python_host_cpu_etc.py | Collection/All | Python | None | Host cpu, memory, disk etc. |
| chk_004_clf_bash_ss.py | Collection/Filter | bash | None | Listening ports with ss command |
| _chk_005_cld_bash_sudo_ufw.py | Collection/Depend | bash | sudo | Uncomplicated Fire Wall (UFW), DISABLED BY DEFAULT AS REQUIRES CERTAIN SUDO PRIVILEGES, remove leading "_" character to activate |
| _chk_006_cld_bash_data_sudo_lsof.py | Collection/Depend | bash | sudo, data file | Outgoing port connections with lsof command, DISABLED BY DEFAULT AS REQUIRES CERTAIN SUDO PRIVILEGES, remove leading "_" character to activate |
| chk_007_clf_debian_ubuntu_unattended_upgrades.py | Collection/Filter | bash | None | Debian based package "unattended-upgrades" is installed, enabled and active |
| chk_008_clf_rhel_dnf_automatic.py | Collection/Filter | bash | RHEL only | RHEL based package "dnf-automatic" is installed, enabled and active |

<br/>
<br/>

### Types of checks

There are 3 types of checks you can create:

* **Bash script** based,
* **Python library or API based** based,
* **Collection** based

All these checks are created the same way:

* They are written as a *Python* **class** which inherits, from the corresponding *MonTTY* check classes

<br/>
<br/>

#### Check inheritance

Your check first inherits from the MonTTY **RootCheck** class

This marks your check class for MonTTY to load it, so the check can be run. There should only ever be *one* class in a check file, that inherits from *RootCheck*

Your check will then **also** inherit from one of the following:

* Checks based on a bash script - will inherit from class **BashCheck**,
* Checks based on a Python Library or API - will inherit from class **PythonCheck**,
* Checks based on a *collection* of bash or Python checks - will inherit from one of the **collection** check classes

Each of these checks is described in a following section

<br/>
<br/>
<br/>
<br/>

## 4 - CLASS "BashCheck"

This class allows you to base you check on a bash script

You create the required bash script to do the check, and store it under the **BASH_SCRIPTS** directory, under CHECKS within the MonTTY project directory

<br/>
<br/>

### Simplest case - constructor only method

In the simplest case, you just provide a Python constructor method for your class __init__()

#### arguments

This constructor requires two or more arguments:

* First argument is the **header_title** - which is effectively the "description" for the check. You are limited to 65 characters
* Second argument is the **bash script** to be run
    * The bash script to be run, must exist under directory **MonTTY project directory/CHECKS/BASH_SCRIPTS**
    * The script name:
        * Is restricted to length: 0 < length <= 64
        * Does not start with a /
        * Does not contain double slashes (//).
        * Allows slashes to separate directories 
        * Is restricted to valid Linux filename characters
    * Any script arguments:
        * Are each passed as a separate argument
        * Are each restricted to length: 0 < length <= 128

<br/>
<br/>

### Bash script exit status code and MonTTY check status

MonTTY automatically captures the exit status code of the bash script, and it will set the check status accordingly for you:

* Exit status code **0** -> MonTTY status **OKAY**
* Exit status code **255** -> MonTTY status **WARN**
* Exit status code **254** -> MonTTY status **NA**
* Exit status code **1..253** -> MonTTY status **ALERT**

<br/>
<br/>

### Bash script stdout and stderr capture

MonTTY automatically captures the *stdout* and *stderr* output from the bash script, and by default displays them in the check report display on the screen with the MonTTY Monitor app

<br/>
<br/>

### Override MonTTY setting the check status

If you do not want MonTTY to just use the bash script exit status code, to set the check status - you can override method:

* **_check_result(command_exit_code:int, command_output:str) -> Status:**

In this method, you can decide what the check status should be

You get as an argument, the bash script output - this is what you typically use to determine the status your self

You also get as an argument, the bash script exit status code, which might also help determine what the status of the check should be

<br/>
<br/>

### Override MonTTY displaying the bash script output

If you want to control what the check out put should be, and not just use the output from the bash script - you can override method:

* **_get_command_output(status:Status, command_output:str) -> str:**

One use case in overriding this method, is to just suppress the output - if the check status was OKAY. This helps keep the check report *"cleaner"* when being displayed, especially if the report has a number of check results

<br/>
<br/>

### Summary

```
                         .-----------.  .-----------.
   MonTTY                | RootCheck |  | BashCheck | <- You must inherit from MonTTY RootCheck and BashCheck 
                         '-----------'  '-----------'
                              ^              ^
                              |              |
                              '--------------'
                                      |
                                      |   ...   inheritance
                                      | 
                          .-----------------------.
   Your Check             |   <Your check class>  | <- You provide your check ...
                          '-------------------------------------------------,
                           | __init__(header_title: str, bash_script: str,  |
                           |     *arguments: str, level_index: int = None)  |
                           '------------------------------------------------'
                                  ^
                                  |
                       .- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - .
                       | _check_result(command_exit_code:int, command_output:str) -> Status | <- OPTIONAL
                       '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '
                                  ^
                                  |
                       .- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -.
                       | _get_command_output(status:Status, command_output:str) : -> str |    <- OPTIONAL
                       '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'

```

<br/>
<br/>
<br/>
<br/>

## 5 - CLASS "PythonCheck"

Allows you to base you check on a Python *library,* *API* or just Python code in general

You can place all the Python code for the check, in the check file

However you can factor some of the Python code, and place it in a separate file as a Python package/module under the **PYTHON_LIBS** directory, which is under the CHECKS directory


### Constructor

You need to add a constructor method to your check class, which calls the super classes constructor "__init__" 

In calling the super class constructor set argument(s):
* **header_title** - which is the "description" for the check. You are limited to 65 characters

<br/>
<br/>

### Override method "_run_class"

You need to override this method, so you can provide the Python code to *perform* the check's logic. Here you will typically call the library or API you are basing your check around

<br/>
<br/>

### Override method "_set_class_result"

You need to override this method, so you can add code to determine the status of the check, and provide any output from performing the check

Use the parameters provided:

* **status** - is a Status object, that you just have to set the status value (such as OKAY) for the check
* **body** - is a CheckBody object that allows you to set any *output* from the check

<br/>
<br/>

### Summary

```
                         .-----------.  .-------------.
   MonTTY                | RootCheck |  | PythonCheck | <- You must inherit from MonTTY RootCheck and PythonCheck 
                         '-----------'  '-------------'
                              ^                ^
                              |                |
                              '----------------'
                                      |
                                      |   ...   inheritance
                                      | 
                          .------------------------.
   Your Check File        |   <Your check class>   |
                          '---------------------------------------------------------------------,
                           | __init__(header_title : str, level_index=None)                     |   <- OPTIONAL
                           |--------------------------------------------------------------------|
                           | _run_class() : None                                                |   <- REQUIRED
                           |--------------------------------------------------------------------|
                           | _set_class_result(self, status: Status, body: CheckBody) -> Status | <- REQUIRED
                           '--------------------------------------------------------------------'

```

<br/>
<br/>
<br/>
<br/>

## 6 - COLLECTION CHECKS

Collection checks, allow you to build your check - from a **collection** of *sub-checks* based on:

* BashCheck,
* PythonCheck
* Other collection checks

<br/>
<br/>

### Creating a collection check

* Create a Python class for your check,
* Inherit from the MonTTY RootCheck class, so MonTTY can correctly load your check file,
* Also inherit from one of the MonTTY *collection check* classes, described below
* Finally add you check classes to the collection, by implementing the collection check class' _add_checks method

<br/>
<br/>

### Types of collection checks

There are currently, these types of collection check classes:

<br/>

No dependency on prior checks ...

* **CollectAllCheck**
    * Runs **all** checks in the collection sequentially in the order added - irrespective of the completion status of prior checks
    * The check gets the highest status status, of any of the checks run:
        * (Highest: ALERT -> WARN -> OKAY -> NA :Lowest)
    * Use when checks **do not** depend on each other

<br/>
<br/>

Dependent on prior checks ...

* **CollectDependCheck**
    * Runs all checks sequentially in the order added, **only** if the prior check completion status *was* OKAY 
    * Else the check exits, and takes the status of the prior check
    * Use when checks, depend on each prior check
    * It is recommended, you restrict the states of the checks in the collection, to be either *ALERT* or *OKAY*

<br/>

* **CollectFilterCheck**
    * Intended to allow for **selectively** running a check
    * A check only runs, if its prior check is successful, having status OKAY
    * The prior check acts as a "filter"
    * You should make the prior "filter" check, return a status of OKAY or NA, and not ALERT
    * Use when checks **should only run** - if a prior check passes

<br/>
<br/>      

```
                         .-----------.  .---------------------------------.
   MonTTY                | RootCheck |  | Collect[All|Depend|Filter]Check | 
                         '-----------'  '---------------------------------'
                              ^                         ^
                              |                         |
                              '-------------------------'
                                       |
                                       |   ...   inheritance
                                       | 
                           .------------------------.
   Your Check File         |   <Your check class>   |
                           '-------------------------------------------------------,
                            | __init__(header_title: str, level_index: int = None) | <-- REQUIRED
                            |------------------------------------------------------|
                            | _add_checks(checks : list[Check]) : None             | <-- REQUIRED 
                            '------------------------------------------------------'

```

<br/>
<br/>

### Constructor parameter *"level_index"*

A number of the check constructors, take an optional parameter **"level_index:int"**

You typically only set this for checks, that **belong to** a collection check

It indicates the *level* of a check form 0 to 5, where:
* Level 0 is the highest or **root** level
* levels 1 to 5 are meant to indicate *nesting* of "sub-checks" (checks belonging to a collection)

MonTTY gives visual indications (such as indenting), when displaying check reports that contain sub-checks

