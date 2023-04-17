# ClockInOut (Attos) :fire:

Automatic login or log out.<br>
Also after execution, it stores your login/logout time in a CSV sheet.<br>
:loud_sound: Insert in the timeclocker_config.ini your account data and URL.
Run the install script

Start with batch script or powershell.
You need to give one arg that represents the call that the script should do.
possible args are: in, out, salden.

## Examples:
### Python:

Login:
```
python Main.py in
```

Logout:
```
python Main.py out
```

Salden:
```
python Main.py salden
```

### Bat example:
Rigt click on one of the .bat files, edit with notepad or any editor.
In the first line after "cd" change the path to your path where the Main.py script is located.
Save file. Do this for Login.bat, Logout.bat and Salden.bat
Now you can use it with double click on the desired file.
