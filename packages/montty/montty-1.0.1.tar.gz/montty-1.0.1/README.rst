MonTTY
======

Links
-----

* Open Source MIT license: `LICENSE <https://github.com/GwynDavies/montty/blob/main/LICENSE>`_
* Installation: `INSTALLATION.md <https://github.com/GwynDavies/montty/blob/main/INSTALLATION.md>`_
* Documentation: `docs <https://github.com/GwynDavies/montty/tree/main/docs>`_
* Source: `src/montty <https://github.com/GwynDavies/montty/blob/main/src/montty>`_
* Issues: `issues <https://github.com/GwynDavies/montty/issues>`_
* Contributing: `CONTRIBUTING.md <https://github.com/GwynDavies/montty/blob/main/CONTRIBUTING.md>`_


Disclaimer
----------

All trademarks, service marks, and product names mentioned in this document are the property of their respective owners


Purpose
-------

MonTTY stands for Monitoring TTY.

It is a tool for Linux hosts, that:

* Allows you to create custom system and cybersecurity checks - using bash or Python scripts,
* Provides the check results in a terminal/console format, allowing you to monitor and review the results.

Check results for MonTTY look like this:

* `Check report screen display <https://github.com/GwynDavies/montty/blob/main/docs/images/screenshot.png>`_


Overview
--------

MonTTY consists of a set of Python applications that run on Linux hosts, to perform system and cybersecurity checks that you write. It is installed into a Python virtual environment to avoid affecting the system's Python installation.

MonTTY consists of 4 Python applications or "apps":

* Checker app,
* Manager app,
* Monitor app,
* Deployer app.

A Linux server is designated as the "MonTTY server". This runs the Manager and Monitor apps.

The Checker app runs on the Linux hosts to be checked. It can also run on the MonTTY server, when it is known as a "local checker".

The Monitor app displays the check results, and runs on the MonTTY server.

The Checker and Manager apps, run automatically using Linux cron jobs.


Checker app
-----------

The Checker app runs the check scripts (written in Python or bash), on Linux hosts to be checked.

These check results are packaged into "check reports", and transferred to the MonTTY server using SCP.

The check report status, can be either:

* ALERT, 
* WARN, 
* OKAY, 
* or NA.

The check report's status, is  determined by the highest status - of individual checks it contains.

A few example check scripts are supplied with MonTTY. These are just basic somewhat contrived examples, to serve as demonstrations - of how checks can be written.


Manager app
-----------

The Manager app organizes and moves check reports into directories based on their status.

Reports with a status of WARN, OKAY, or NA are deleted after their Time-to-Live (TTL) expires (5 minutes). ALERT status reports are never deleted automatically, and must be deleted by the user.


Monitor app
-----------

The Monitor app displays check reports in a terminal/console, prioritizing ALERT status reports, then WARN, and finally OKAY/NA reports.

The reports are viewed on the MonTTY server, either by the user being locally logged in, or by an SSH connection.

Users can then view the reports, and interact with them using simple commands.


Deployer app
------------

The Deployer app finishes up the install of MonTTY. It mainly extracts necessary files and directories from the MonTTY Python package distribution, into the MonTTY project directory.

The Deployer app, works on the concept of the MonTTY "project dir". This is the directory where the MonTTY Python distribution is interred into a Python virtual environment. This exists on the MonTTY server host, and all checked hosts.

The Deployer app unpacks from the MonTTY Python distribution, the following directories:

* "CHECKS", where the MonTTY checks are stored, along with their associated support files. MonTTY ships with some example check files,
* "REPORTS", where the check report files are stored while they are processed.

Also unpacked are two bash shell scripts:

* "run.sh", runs all MonTTY apps,
* "spy.sh", allows you to monitor the REPORTS directory as MonTTY operates.


Apps schematic
--------------

This diagram illustrates how the MonTTY apps, interrelate:

* `MonTTY apps schematic <https://github.com/GwynDavies/montty/blob/main/docs/images/montty_app_schematic.png>`_


