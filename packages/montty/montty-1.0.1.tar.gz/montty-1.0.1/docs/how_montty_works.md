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

## 2 - PURPOSE

MonTTY (**Mon** *itoring* **TTY**), allows you for **Linux Hosts** to:

* Create you own system and cybersecurity checks 
* These checks can be based on **bash** or **Python** scripts
* You can then view/monitor reports of the check results, in a terminal or console

<br/>

A *check report* in MonTTY looks like this:

```
MonTTY    OKAY  Host: fakehost2        IPv4: 192.0.2.0        At: October 26, 2024 01:34:20
1.0.0     [q]uit [d]elete [^s]pause [^q]resume     Report: 69bc........................efbe

    Net       :  errin   :   0
                 errout  :   0
                 dropin  :   0
                 dropout :   0
 (+) SystemBootDataCheck                                              .(OKAY).
    Boot      :  25th October 2024 12:58:36

chk_004_clf_bash_ss.py - Check FILTER                                  (OKAY)
 (f) Filter HOST not equal "fakehost1"                                .(OKAY).
    -> Test host_not_eq fakehost1
 (f) CheckSSPorts - LISTENING TCP PORTS                               .(OKAY).


SUMMARY:

     chk_001_bash_listening_ports_with_ss.py - LISTENING TCP PORTS          (OKAY)
     chk_002_python_host_cpu.py - HOST CPU                                  (OKAY)
     chk_003_cla_python_host_cpu_etc.py- HOST CPU ETC.                      (OKAY)
     chk_004_clf_bash_ss.py - Check FILTER                                  (OKAY)

```

<br/>
<br/>
<br/>
<br/>

## 3 - OVERVIEW

<br/>

MonTTY is built as a set of Python applications or *apps* 

These run on:

* Linux host(s) to be checked,
* A designated Linux MonTTY server host

<br/>
<br/>

Generally the hosts will need to have:

* An up-to-date mainstream Linux distribution installed (E.g. Debian, Ubuntu LTS and RHEL)
* A supported Python version (see **installation instructions** later for minimum version)
* You can use the system Python installation, if the version is high enough, as: 
    * Package downloads are done with **pip** into a **virtual environment**, leaving the system Python installation unaffected

<br/>
<br/>

You view the check reports, by connecting to the MonTTY server host, via **SSH client** using a terminal or console

```
  .-----------.                 
  | Linux     |-.                 .-----------.             .------------------.
  | Checked   | |-.     SCP       | Linux     |    SSH      | User terminal or |-.      0
  | Host(s)   | | |  -------->    | MonTTY    |  <--------  | console          | |     /|\
  '-----------' | |               | Server    |             |                  | |      |
    '-----------' |               | Host      |             '------------------' |     / \
     '------------'               '-----------'               '------------------' 
                                                        
        ^                             ^   
        |                             |
MonTTY Checker App       MonTTY Manager, MonTTY Monitor Apps

```

<br/>
<br/>

### Python, pip and virtual environments

MonTTY apps are written in Python and **distributed as a single Python package**, that you install with the Python utility [pip](https://pypi.org/project/pip/)

You **have** to use a Python [virtual environment (PEP 405)](https://peps.python.org/pep-0405/) for MonTTY

A benefit of using a Python virtual environment, is that you can install MonTTY and other associated Python packages, without affecting the system Python installation 

<br/>
<br/>

### Internet access:

A Linux host will need internet access, to download Python packages with pip

Also if you do use a git project for the MonTTY project directory - for the sending/receiving files to the Git server


```

   MonTTY
      |       Installs with pip
      v
 .----------.
 | Python   |
 | virtual  | <---- Created with Python
 | env      |
 '----------' 

```
<br/>
<br/>

### Project directory

Once MonTTY is installed into the Python virtual environment, you deploy its required files and directories, using an app called the **MonTTY Deployer**

The MonTTY server host, and the MonTTY checked hosts, all have the same project directory structure - but make different usage of it

<br/>
<br/>

#### Directories

The MonTTY Deployer app unpacks 2 directories:

* **REPORTS** is used by the:
    * MonTTY Manager app, to **receive and manage** the check reports,
    * MonTTY Monitor app, for users to **view** the check reports

* **CHECKS** is where you write and keep your check files, that perform your checks

It is recommended, that the MonTTY **project directory is managed by git**, so you can control the development and storage of your check files

<br/>
<br/>

#### Bash scripts

Also unpacked, are 2 bash scripts:
* *run.sh* is used to run the various MonTTY apps
* *spy.sh* allows you to see what is "happening", in the REPORTS directories

<br/>
<br/>

```

 .--------------------------------------------------------------------------------------------.
 | MonTTy project directory - for all Linux hosts:                                            |
 |                                                                                            |
 |                                                                                            |
 |   .----------.                                                                             |
 |   | Python   |                             .---->  run.sh                                  |
 |   | virtual  |                             .---->  spy.sh                                  |
 |   | env      |                             |                                               |
 |   |          |                             |---->  CHECKS/  <-- You develop and keep your  |
 |   '----------'                             |                    checks here, there are     |
 |        |                                   |                    also some examples         |
 |        |                                   |                                               |
 |        |                                   |---->  REPORTS/ <-- Check reports are placed   |
 |        |              Unpack               |          |         under here                 |
 |        |                                   |          |                                    |
 |        |           .----------.            |          |--  _input                          |
 |        '-----------| MonTTY   |------------'          |                                    |
 |                    | Deployer |                       |--  _report                         |
 |                    '----------'                       |                                    |
 |                                                       |--  _warn                           |
 |                                                       |                                    |
 |                                                       '--  _alert                          |
 |                                                                                            |
 '--------------------------------------------------------------------------------------------'

```

<br/>
<br/>

### Communication

The MonTTY checked hosts, need to be able to send the check reports - to the MonTTY server host

Also users need to be able to view check reports on the MonTTY server

MonTTY uses the **SSH/SCP** when check data is in *motion*

* The MonTTY Checker on checked hosts, sends the check reports to the MonTTY server using **SCP**
* To allow this to be automated, each checked host - must have a *public/private* key-pair, with the *public* key deposited on the MonTTY server host. This serves as the authentication, for the SCP transfer

<br/>
<br/>

### Automation with  **cron**

Currently two of the MonTTY apps (Checker, Manager), run on a continual basis

MonTTY simply uses cron jobs, that you configure to automate their running

<br/>
<br/>
<br/>
<br/>

## 4 - CHECKER APP 

<br/>

### Checks and reports

The MonTTY Checker app runs the check file(s) 

It then packages the check results in a file as a **check report**, which it sends to the MonTTY server:
* Using the **SCP** command
* Depositing them in the MonTTY project directory - under **REPORTS/_input**

<br/>
<br/>

### How checks are run

A check file must:

* Be placed in the MonTTY project directory, under the **CHECKS** directory,
* Have a filename that:
    * Starts with **chk**
    * Has a .py extension
    * E.g. **chk_005_cld_bash_sudo_ufw.py**

By default, all check files that match the above criteria are run, by the MonTTY Checker app 

You can override this behavior, to **selectively run checks** as described below

A quick way to *"disable"* a check file, is to just rename the file to have a leading **_** character

E.g. **_chk_005_cld_bash_sudo_ufw.py**

This convention is used with the example check files provided with MonTTY

<br/>
<br/>

### Selectively running checks

The MonTTY Checker app, requires an argument that specifies **tags** - to control which checks are run

* If you give an **empty string** for this argument - then all available checks are run
* Alternatively, if you do give **one or more tags** - then only checks **having those tags**, are run

To get the default behavior, of running all the available eligible checks, you would run the Checker app, with the *tags* argument set to an **empty string** 

E.g. 

```
       Runs the MonTTY Checker app "locally" 
        (on the MonTTY server)
                |
                v
$ ./run.sh local_chk chk "" 
                          ^
                          |
                      Empty tags argument

```

<br/>
<br/>

Along with *check* files in the MonTTY project directory's CHECKS directory, you can have a CSV file called **checks.csv**

It is in this file, that you associate **tags** with **check file name(s)** 

For example, in the *checks.csv* file, you might have:

```
check_file_name,tags
chk_001_bash_listening_ports_with_ss.py, bash_check python_check
chk_002_python_host_cpu.py, python_check
chk_003_cla_python_host_cpu_etc.py, collect_check python_check
chk_004_clf_bash_ss.py, collect_check bash_check

```

This CSV file, first has a header line that describes the file's CSV format:

```
check_file_name,tags

```

Then each subsequent line consists of:

```
<check file name>, <one or more tags, separated by spaces>

```

If a check file name, has **one or more** of the tags specified in the command to run the MonTTY Checker app - that that check file will be run

If a check file in the checks.csv file does not have **any** of the tag values specified - then that check will not be run

<br/>
<br/>

### Check status

Each check result, has a status from **highest** to **lowest** of:

* **ALERT**
* **WARN**
* **OKAY**
* **NA**

<br/>
<br/>

### Check reports

The results of running each check, are collected together in a **check report**

The **report itself has a status** - which it takes the *highest* individual check result status, of its' checks as follows:

* If any check has a status of *ALERT*, the report will have status of *ALERT* 
* Else: 
    * If any check has a status of *WARN*, then the report will have status of *WARN*
* Else:
    * If any check has a status of *OKAY*, then the report will have a status of *OKAY*
* Otherwise:
    * The report will have a status of *NA*

<br/>
<br/>
<br/>
<br/>

## 5 - MANAGER APP 

The MonTTY Manager app manages the life-cycle of check reports, received from the checked hosts' Checker apps

These reports are received in the MonTTY Manager's project directory, under the REPORTS/_input directory

It moves the reports to:

* The **_report** directory  - if they have a status or **NA** or **OKAY**
* The **_warn** directory    - if they have a status of **WARN**
* The **_alert** directory   - if they have a status of **ALERT**

<br/>
<br/>

### Expired reports and Time-to-Live (TTL)

Check reports are stamped with a Time-to-Live (TTL) value. Currently this is set to **5 minutes**

Reports with a status of **WARN, OKAY or NA** are removed by the Manager app - when their TTL expires

Reports with a status of **ALERT** never expire

The user must delete these reports, using the MonTTY *Monitor* app

<br/>
<br/>
<br/>
<br/>

## 6 - MONITOR APP

The MonTTY Monitor app, displays check reports one at a time, in a terminal or console as follows:

* All the **ALERT** status reports are displayed first
    * The user can delete these reports, once they have acted on the alert according to their processes or procedures

* If there are no ALERT reports left, then any reports having status of **WARN** are displayed, until either:
    * The user deletes them, or 
    * They exceed their TTL, and the Manager app deletes them

* Finally reports with status **OKAY** or **NA** are displayed, until either:
    * The user deletes them, or 
    * They exceed their TTL, and the Manager app deletes them

<br/>
<br/>

### Monitor app visual display

<br/>

A *header* is displayed for the current check report, giving details of:

* Its status
* Checked host it is from
* At when the report was generated

 A limited *menu* of commands the user can initiate is also displayed, which respond to their corresponding keystrokes

<br/>

A vertical scrolling *body* is displayed, giving details of:

* Each of the checks contained in the check report
* A summary of these checks at the end of the scrolling


#### Header display

```
    Status of report             Checked host                     When the report was 
    being displayed                   |                            was created 
            |              .---------------------.                 (local date/time)
            |              |                     |                         |
            |              |                     |                         |
            |           hostname             IPv4 address                  |
            |              |                     |                         |
            v              v                     v                         v

MonTTY    OKAY  Host: fakehost2        IPv4: 192.0.2.0        At: October 26, 2024 01:34:20
1.0.0     [q]uit [d]elete [^s]pause [^q]resume     Report: 69bc........................efbe
  ^                       ^                                               ^
  |                       |                                               |
MonTTY                   User                                      Report ID (GUID)
Version                  Commands

```

<br/>
<br/>

#### Body display

```
 ...

    Net       :  errin   :   0
                 errout  :   0
                 dropin  :   0
                 dropout :   0
 (+) SystemBootDataCheck                                              .(OKAY).
    Boot      :  25th October 2024 12:58:36

chk_004_clf_bash_ss.py - Check FILTER                                  (OKAY)
 (f) Filter HOST not equal "fakehost1"                                .(OKAY).
    -> Test host_not_eq fakehost1
 (f) CheckSSPorts - LISTENING TCP PORTS                               .(OKAY).


SUMMARY:

     chk_001_bash_listening_ports_with_ss.py - LISTENING TCP PORTS          (OKAY)
     chk_002_python_host_cpu.py - HOST CPU                                  (OKAY)
     chk_003_cla_python_host_cpu_etc.py- HOST CPU ETC.                      (OKAY)
     chk_004_clf_bash_ss.py - Check FILTER                                  (OKAY)

```    

<br/>
<br/>
<br/>
<br/>

## 7 - DEPLOYER APP

<br/>

The MonTTY Deployer app, makes a deployed instance of MonTTY available for use

It currently creates files and directories in the MonTTY **project directory**, by extracting them from the installed MonTTY pip package

<br/>
<br/>
<br/>
<br/>

## 8 - APPS SCHEMATIC

```
      MonTTY Checked Host(s)                                    MonTTY Server Host              

.----------------------------------.           .-----------------------------------------------------.
|                                  |.          |                                                     |
|                                  | |         |                                                     |
|  .- - - - - - - - - - - - - - .  | |         |  .- - - - - - - - - - - - - - - - - - - - - - - -.  |
|  ' Git project dir            '  | |         |  ' Git project dir                               '  |
|  '                            '  | |         |  '                                               '  |
|  '          CHECKS            '  | |         |  '                 REPORTS                       '  |
|  '            |               '  | |         |  '                    |                          '  |
|  '  .- - - - -| - - - - - -.  '  | |         |  '       .------------+---+-------+-----.        '  |
|  '  '         |            '  '  | |         |  '       |                |       |     |        '  |
|  '  '         |            '  '  | |         |  '       |                |       |     |        '  |
|  '  '         v            '  '  | |         |  '       |                |       |     |        '  |
|  '  '  .------------.      '  '  | | Reports |  '       |                |       |     |        '  |
|  '  '  |  Checker   | ---------------------------->  _input     .-->  _report _warn _alert      '  |
|  '  '  '------------'      '  '  | |  (SCP)  |  '       |       |        |       |      |       '  |
|  '  '    { crontab }       '  '  | |         |  '       |       |        |       |      |       '  |      
|  '  '                      '  '  | |         |  '       |       |        |       |      |       '  |  Monitor    
|  '  ' Python virtual env   '  '  | |         |  '  .- - | - - - |- - - - | - - - | - - -| - -.  '  |  Reports
|  '  '- - - - - - - - - - - '  '  | |         |  '  '    |       |        |       |      |    '  '  |      
|  '                            '  | |         |  '  '    v       |        v       v      |    '  '  |     0
|  '                            '  | |         |  '  '  .-----------.   .-------------------.  '  '  |    /|\
|  '- - - - - - - - - - - - - - '  | |         |  '  '  |  Manager  |   |  Monitor          |<-----------  |
|                                  | |         |  '  '  '-----------'   '-------------------'  '  '  |    / \
|                                  | |         |  '  '    { crontab }       { ncurses }        '  '  |   
|                                  | |         |  '  '                                         '  '  |   (SSH)
|                                  | |         |  '  ' Python virtual env                      '  '  |
|                                  | |         |  '  '- - - - - - - - - - - - - - - - - - - - -'  '  |
|                                  | |         |  '                                               '  |
|                                  | |         |  ' - - - - - - - - - - - - - - - - - - - - - - - '  |
|                                  | |         |                                                     |
'----------------------------------' |         '-----------------------------------------------------'
  '----------------------------------' 

```

