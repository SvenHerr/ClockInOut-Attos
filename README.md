# Timeclocker Automation => ClockInOut (Attos) :fire:

This Python script automates time booking using Selenium WebDriver.<br>
Also after execution, it stores your login/logout time in a CSV sheet.<br>
:loud_sound: Insert in the timeclocker_config.ini your account data and URL.
Run the install script

Start with batch script or powershell.
You need to give one arg that represents the call that the script should do.
possible args are: in, out, salden.

## Features

- Supports logging in and logging out of the time tracking system.
- Retrieves booked time and balance information.
- Logs the data to a CSV file.
- Sends email notifications with booking status.

## Installation

1. Clone the repository or download the source code.
2. Install the required Python libraries using pip:

   ```shell
   pip install selenium webdriver_manager email configparser

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

## Requirements

- Python 3.x
- Selenium WebDriver
- webdriver_manager
- email
- configparser
- csv
- os
- Chrome WebDriver (automatically managed by webdriver_manager)
