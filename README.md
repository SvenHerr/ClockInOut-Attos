# ClockInOut (Attos)

Automatic login or log out.
Also after execution, it stores your login/logout time in a CSV sheet.
Insert in the timeclocker_config.ini your account data and URL.
Run the install script

Start with batch script or powershell.
You need to give one arg that represents the call that the script should do.
possible args are: in, out, salden.

Examples:

Login with python:
python Main.py in

Logout with python:
python Main.py out

Salden with python:
python Main.py salden

Bat example:
Rigt click on one of the .bat files, edit with notepad or any editor.
In the first line after "cd" change the path to your path where the Main.py script is located.
Save file. Do this for Login.bat, Logout.bat and Salden.bat
Now you can use it with double click on the desired file.