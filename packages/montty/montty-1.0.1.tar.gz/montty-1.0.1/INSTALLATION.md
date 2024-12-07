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

## 2 - REQUIREMENTS

<br/>

### Host requirements

MonTTY is built as a set of Python applications or *apps* 

These run on:

* Host(s) to be checked,
* A designated host to server as the MonTTY server host, where check reports will be collected and are viewed from

<br/>

MonTTY runs on **Linux hosts only**

Generally the hosts will need to have:

* An up-to-date mainstream Linux distribution installed (E.g. Debian, Ubuntu LTS and RHEL)
* The MonTTY server will need to be capable to accept SSH/SCP requests
* All MonTTY checked hosts will need to be capable of making SCP requests 

<br/>
<br/>

### Python requirements

MonTTY requires all hosts to have Python version **3.9** or greater installed

You can use the system Python installation, if the version is high enough, as: 
* You **have to use a virtual environment** with MonTTY
* Package downloads are done with **pip** into a **virtual environment**, leaving the system Python installation unaffected

<br/>
<br/>

### Other requirements

<br/>

You will need **some** familiarity with Linux system administration activities, such as:

* Accessing **super user privileges (E.g. via sudo)**
* Creating user accounts
* Configuring crontab for a user
* Installing any needed system packages
* Creating public/private key-pairs
* Using SSH and SCP
* Optionally - enabling *sudo* features for a user

<br/>
<br/>
<br/>
<br/>

## 3 - STEPS FOR ALL HOSTS

<br/>

You will need to perform these steps using a terminal or console, on the **all MonTTY hosts**:

* The designated Linux MonTTY server host
* Each Linux MonTTY checked host

<br/>
<br/>

### Git

- [ ] *Recommended* - Create Git project, on server such as *GitHub* or *GitLab*, etc.
- [ ] *Recommended* - Check the command line git client is installed

Use of git to control the check you develop is recommended

If you do want to use git, check it is installed as follows 

You should be able to install it, your Linux distribution's package manager:

```
Check git is installed
$ git -v

  git version x.xx.x

```

<br/>
<br/>

### Create MonTTY user account

- [ ] **Required** - Create Linux user account, for the MonTTY user (e.g. mtyuser)
- [ ] **Required** - Ensure MonTTY user's shell is bash
- [ ] **Required** - Ensure crontab is available, to the MonTTY user account

```   
$ sudo useradd -m <MonTTY user>
$ sudo passwd <MonTTY user>

Change MonTTY user's shell to bash if it is not already
$ sudo chsh -s /bin/bash <MonTTY user>


<Login or become the created MonTTY user>

$ crontab -l
  no crontabs for mtyuser


<As another user with admin privileges>

$ sudo crontab -u <MonTTY user> -l
  no crontabs for mtyuser


Examples:
    $ sudo useradd -m mtyuser
    $ sudo passwd mtyuser
    $ sudo chsh -s /bin/bash mtyuser


    $ crontab -l
      no crontabs for mtyuser
    

    $ crontab -u mtyuser -l
      no crontabs for mtyuser

```

<br/>
<br/>

### Enable specific sudo privileges, for MonTTY user account

- [ ] **Optional** - Enable specific sudo privileges, for MonTTY user account

If you want the MonTTY user to be able to use **sudo** for commands in some of the example checks, you will need to grant the *required explicit sudo privileges*

Also, these explicit privileges need to be available without giving a password - in order for MonTTY to run the required *sudo* check command(s)  automatically

You can grant these sudo privileges as described here in two (possibly other) different ways:

* Creating a file for the MonTTY user under /etc/sudoers.d
* Alternatively using 'visudo'

<br/>

#### Creating a file for the MonTTY user under /etc/sudoers.d

On recent Linux distributions, you can navigate to the **/etc/sudoers.d** directory and:

* Create a file, usually with the name of the user, to grant sudo privilege(s)
* However, this convention is not actually necessary, as sudo will scan all files in this directory as needed

For example, to allow the *MonTTY user* to perform the commands, for the two provided example checks, that require *sudo* you would add :

```
<MonTTY user> ALL=NOPASSWD: /usr/sbin/ufw status verbose,/usr/bin/lsof -i

Example:
    mtyuser ALL=NOPASSWD: /usr/sbin/ufw status verbose,/usr/bin/lsof -i

        For provided example check file _chk_005_cld_bash_sudo_ufw.py, add:
            /usr/sbin/ufw status verbose

        For provided example check file _chk_006_cld_bash_data_sudo_lsof.py, add: 
            /usr/bin/lsof -i

```

<br/>

#### Alternatively using 'visudo'

As an alternative, you can edit the **Sudoers File** - preferably with the **visudo** command:

```
$ sudo visudo

```

<br/>

Inside the file, you as above grant the privilege(s)

For example, to allow the MonTTY user, to perform the commands for the two provided example checks, that require *sudo* you would add :

```
<MonTTY user> ALL=NOPASSWD: /usr/sbin/ufw status verbose,/usr/bin/lsof -i


Example:
    mtyuser ALL=NOPASSWD: /usr/sbin/ufw status verbose,/usr/bin/lsof -i

        For provided example check file _chk_005_cld_bash_sudo_ufw.py, add:
            /usr/sbin/ufw status verbose

        For provided example check file _chk_006_cld_bash_data_sudo_lsof.py, add: 
            /usr/bin/lsof -i

```

<br/>
<br/>

### Check Python **3.9** or higher installed

- [ ] **Required** - Login, or become the *MonTTY user* via 'sudo':
- [ ] **Required** - Check Python **3.9** or higher is installed

<br/>

Just login as the *MonTTY user* or become the user:

```
$ sudo - <MonTTY user>

Example:
    $ sudo - mtyuser

```

<br/>

Check Python is installed (note the 'V' is capitalized):

```
$ python3 -V
or
$ python -V

```

If Python is not installed, or the version is less than **3.9** - you will need to install it

<br/>
<br/>

### Create the MonTTY project directory 

- [ ] **Required** - A project directory is created for MonTTY

Normally place it under the home directory, of the MonTTY user created above

You can create the project directory by either:

* Using git clone - if you created a git project above
* Manually create the directory

<br/>
<br/>

#### Git "clone" project

- [ ] **Alternative 1 of 2** - If you setup a Git project above, then clone it:

```
$ git clone <URL of git project you created above>`

```

<br/>
<br/>

#### Alternatively just manually create the directory

- [ ] **Alternative 2 of 2** - Just create a directory, if you did not create a git project above

```
$ mkdir <project directory>

Example:

$ mkdir montty

Set the file permissions so the MonTTY user has access to create, edit and run files in this directory

```

<br/>
<br/>

### Setup Python virtual environment

#### Change into project directory

- [ ] **Required** - Change into the project directory

```
$ cd <project directory>

Example:

$ cd montty

```

<br/>
<br/>

#### Create Python virtual environment

- [ ] **Required** - Create a Python virtual environment (venv), in created in the project directory

```
$ python3 -m venv venv

```

<br/>
<br/>

#### Activate Python virtual environment

- [ ] **Required** - Activate the Python virtual environment is activated

```
$ source venv/bin/activate

The terminal prompt should now be prefixed with (venv) and look something like this:

  (venv) <user>:<path> $

```

- [ ] **Required** - Check the shell now shows the virtual environment (venv), you can now use commands **python** and **pip**

```
$ python -V
$ pip -V

Notes: 
    The -V is capitalzed

    You use "python" with a activated virtual env, even if the actual binary program is "python3"
    
```

<br/>
<br/>

### Install MonTTY

<br/>

#### Install MonTTY using pip

- [ ] **Required** - Install MonTTY using pip

Install MonTTY with pip, it should be found and received from [PyPI site](https://pypi.org/project/montty/)

```  
$ pip install montty

  ...
  Successfully installed ...

```

<br/>
<br/>

#### Check MonTTY is available

- [ ] **Required** - Check MonTTY is now available:

```
    $ montty-deployer --help

```

You should see output similar to this:

```
(venv) $ montty-deployer --help

  usage: montty-deployer [-h]

  Initial deployer script for MonTTY, to prepare the project directory.

  options:
    -h, --help  show this help message and exit

```

<br/>
<br/>

#### Unpack MonTTY files and directories

- [ ] **Required** - Unpack MonTTY files and directories

Run the MonTTY deployer app, to unpack the required MonTTY files and directories, for MonTTY's operation

```
    $ montty-deployer

```

<br/>

- [ ] **Check** - The MonTTY files are unpacked

Along with the Python virtual environment directory *venv* - you should now see additional directories and bash shell scripts:

```
$ ls -1
  (Note that is numeral one '1')

CHECKS/
REPORTS/
run.sh
spy.sh
venv

```

<br/>
<br/>
<br/>
<br/>

## 4 - STEPS FOR THE MonTTY SERVER HOST

<br/>

### Configure crontab for MonTTY Manager app

- [ ] **Required** - Configure crontab for the MonTTY Manager app

On the MonTTY server host, add the following line to the MonTTY user's crontab - with the correct MonTTY "project directory"

This will run the MonTTY Manager app every minute (or you can change it to whatever interval you want to use): 

```
$ crontab -e

* * * * *   cd <project directory>; ./run.sh man > manager.log 2>&1

Example:   

    * * * * *   cd /home/mtyuser/montty; ./run.sh man > manager.log 2>&1

``` 

<br/>
<br/>

### Configure crontab entry, for MonTTY Checker app (Local instance)

- [ ] **Required for testing, optional after that** - Configure crontab for the MonTTY Checker app (local instance):


Also add the following line to the MonTTY user's crontab, again with the correct MonTTY "project directory"

This will run the MonTTY Checker app every 10 minutes

This is for testing that MonTTY is working, but you can leave it in operation, if you also want to run checks on the MonTTY server

```
$ crontab -e

*/10 * * * *   cd <project directory>; ./run.sh local_chk "" > local_chk.log 2>&1

Example:   

    */10 * * * *   cd /home/mtyuser/montty; ./run.sh local_chk "" > local_chk.log 2>&1
``` 

<br/>
<br/>

### Check the MonTTY Manager, Checker and Monitor apps are working

#### Create test check report with Checker app

- [ ] **Required for testing** - Create test check report with MonTTY Checker app

In the MonTTY project directory, run the following command:

```
$ ./run.sh local_chk ""

```

<br/>
<br/>

#### Confirm check file is created in the MonTTY Manager app input directory

- [ ] **Required for testing** - Confirm a check file is created under the REPORTS directory

* Initially the check report should be created under the REPORTS/_input directory
* It will then be moved by the MonTTY Manager app, to one of the others directories - depending on its status:
* This should happen in about one minute, if you went with the specified crontab entry in the above steps

If it is not moved, check the file **manager.log** in the project directory for an error

```
$ ./spy.sh

  (Just ignore the ones ending in '_', use CTRL-C to exit))

Every 2.0s: find ./REPORTS       

 ./REPORTS
 ./REPORTS/_input
 ./REPORTS/_input/_
 ./REPORTS/_report
 ./REPORTS/_report/_
 ./REPORTS/_alert
 ./REPORTS/_alert/_
 ./REPORTS/_warn
 ./REPORTS/_warn/_

```

<br/>
<br/>

#### Check MonTTY Monitor app displays the test check report

- [ ] **Required for testing** - Check MonTTY Monitor app displays the test check report

Now run the MonTTY Monitor app, to make sure the check report is displayed

```
$ ./run.sh mon

```

The check report should be displayed

**Press the d keyboard key** to delete the check report - the check report should be deleted

**Press the q keyboard key** to "quit" the MonTTY monitor app

<br/>
<br/>
<br/>
<br/>

## 5 - STEPS FOR *EACH* MonTTY CHECKED HOST

<br/>

Now you have the MonTTY server configured as above, you need to perform the following steps, **on each of the MonTTY checked hosts**

This is so they can generate check reports, and send them to the MonTTY server

<br/>
<br/>

### Become *MonTTY user*

Login as the *MonTTY user* or become the user via 'sudo':

```
$ sudo - <MonTTY user>

Example:
    $ sudo - mtyuser

```

<br/>
<br/>

### Check SCP is installed

- [ ] **Required** - Check SCP is installed

If SCP is not installed, you will need to install it, as per your Linux distribution

```
$ which scp
  /usr/bin/scp

```

<br/>
<br/>

### Generate public/private key-pair

- [ ] **Required** - Generate public/private key-pair

In order for the MonTTY check reports to be sent to the MonTTY server, SCP needs to be able to operate automatically, hence without a password being supplied

We achieve this, by generating a **public/private key-pair** for the MonTTY checked host, and deploying the **public** key on the MonTTY server host

<br/>

The checked host can then, send the check reports using SCP - to the MonTTY server host

Generate a key-pair, in accordance with **your security guidelines and processes** :

```
$ ssh-keygen <options and parameters>

Example:

    $ ssh-keygen -t ed25519 

```

<br/>
<br/>

### Deploy MonTTY checked host public key, to MonTTY designated server

- [ ] **Required** - Deploy checked host public key, to the designated MonTTY server

The public key for the key-pair needs to be deployed on the MonTTY server:

* In the **authorized_keys** file, 
* Under the MonTTY user's <home>/.ssh directory
* Example:
    * /home/mtyuser/.ssh/authorized_keys

<br/>
<br/>

#### Ensure .ssh directory exists for the *MonTTY user* on the server host

- [ ] **Required** - Ensure .ssh directory exists for the *MonTTY user* on the server host

The directory to deploy the MonTTY checked host(s) keys to, needs to exist for the *MonTTY user* on the server host - if we are to be able to deploy the checked host public keys to

This directory will have been created for you, if you have generated an ssh key for the *MonTTY user* on the server host

However, you can also create the directory manually **if it does not exist** - as the *MonTTY user* on the server host:

```
$ cd

$ mkdir -p .ssh
$ chmod 700 .ssh/
$ ls -al

$ cd .ssh/
$ touch authorized_keys
$ chmod 600 authorized_keys

```

<br/>
<br/>

#### Copy ssh key to MonTTY server

- [ ] **Required** - Copy ssh key to MonTTY server

How you get the *MonTTY user* key to the server's authorized_keys file, depends on the access your user has

<br/>

##### Check interactive ssh login

If the server allows interactive login for ssh, then you can use the steps below

Otherwise you will have to find another way to get the *MonTTY user's* public key onto the server, possibly using another user, who already has their key on the server

You can check the availability of interactive login for ssh on the MonTTY server as follows:

```
$ sudo vim /etc/ssh/sshd_config

Check setting 'KbdInteractiveAuthentication':

 ...
 # Change to yes to enable challenge-response passwords (beware issues with
 # some PAM modules and threads)
 KbdInteractiveAuthentication [yes|no]
 ...

```

If this setting is 'yes', then you could possibly use an interactive ssh login, to copy the public key

If this setting is 'no', then you will probably have to find another way

Do not just change this setting even if you have the access, as it might not be inaccordance
with your organization's  policies and procedures

<br/>

##### Copy public key with interactive login

```
 $ cat ~/.ssh/id_<key type>.pub | ssh <MonTTY user>@<MonTTY server [hostname|ip address] 'cat >> ~/.ssh/authorized_keys'


Example:
 $ cat ~/.ssh/id_ed25519.pub | ssh mtyuser@192.0.2.0 'cat >> ~/.ssh/authorized_keys'

```

<br/>
<br/>

### Check SCP file transfer to the MonTTY server

- [ ] **Required** - Check the user is able to SCP a file to the designated MonTTY server, from the checked host

As the MonTTY user, on the MonTTY checked host:

```
$ cd <MonTTY project directory>/REPORTS/_input

$ touch test_file.txt

$ scp test_file.txt <MonTTY user>@<MonTTY server hostname or IP addr>:<path of MonTTY project REPORTS/_input directory>

Example:
    $ scp mtyuser@192.0.2.0:~/montty/REPORTS/_input 

```

<br/>
<br/>

### Configure crontab entry

- [ ] **Required** - Configure crontab entry, for MonTTY Checker app

As the MonTTY user on the checked host, use the crontab command to add an entry, to run the MonTTY Checker app

```
$crontab -e 

```

Create the following crontab entry:

```
*/10 * * * *   cd <project directory>; ./run.sh chk "" <MonTTY user> <MonTTY server ip or hostname> <MonTTY project dir>/REPORTS/_input > checker.log 2>&1


Example, to run the MonTTY Checker app - every 10 minutes:

*/10 * * * *   cd /home/mtyuser/montty; ./run.sh chk "" mtyuser 192.0.2.0 ~/montty/REPORTS/_input > checker.log 2>&1

```

#### Also adding PATH to crontab

For some of the example checks that ship with MonTTY, I have noticed for some Linux distributions (e.g. RHEL), that I had also to include a **'PATH'** variable setting, in the *MonTTY user's* crontab

In this case, you just need to add a 'PATH' variable before the other crontab entries, for example: 

```
PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin

*/10 * * * *   cd /home/mtyuser/montty; ./run.sh chk "" mtyuser 192.0.2.0 ~/montty/REPORTS/_input > checker.log 2>&1

```

