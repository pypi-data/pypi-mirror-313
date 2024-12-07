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

# Online docs

https://twine.readthedocs.io/en/latest/

More documentation on using Twine to upload packages to PyPI is in the 
Python Packaging User Guide:

    https://packaging.python.org/tutorials/packaging-projects/


<br/>
<br/>
<br/>

# Commands

```
twine upload dist/*

```

Twine will prompt for your username and password.


Like many other command line tools, Twine does not show any characters 
when you enter your password


<br/>

## Note:

If you’re using Windows and trying to paste your username, password, or 
token in the Command Prompt or PowerShell, Ctrl-V and Shift+Insert won’t 
work

Instead, you can use “Edit > Paste” from the window menu, or enable :
“Use Ctrl+Shift+C/V as Copy/Paste” in “Properties” 

This is a known issue with Python’s getpass module
