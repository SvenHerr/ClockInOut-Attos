import os
from configparser import ConfigParser

class ConfigClass:
    def __init__(self, config_ini_path):
        self.config_ini_path = config_ini_path
        self.config = ConfigParser()
        self._load_config()

    def _load_config(self):
        if os.path.isfile(self.config_ini_path):
            self.config.read(self.config_ini_path)
            # Read configuration values
            self.isEmailEnabled = self.config.getboolean("Settings", "isemailenabled", fallback=False)
            if self.isEmailEnabled:
                self.username = self.config.get("Mail-Setting", "username", fallback='')
                self.password = self.config.get("Mail-Setting", "password", fallback='')
                self.sender = self.config.get("Mail-Setting", "sender", fallback='')
                self.receiver = self.config.get("Mail-Setting", "reciever", fallback='')  # typo corrected to "receiver"
                self.smtpServer = self.config.get("Mail-Setting", "smtpserver", fallback='')
                self.smtpPort = self.config.getint("Mail-Setting", "smtpport", fallback=587)
            self.usernameAttos = self.config.get("Account-Settings", "usernameAttos", fallback='')
            self.pwAttos = self.config.get("Account-Settings", "pwAttos", fallback='')
            self.url = self.config.get("Settings", "url", fallback='')
            self.isCSVEnabled = self.config.getboolean("Settings", "iscsvenabled", fallback=True)
            self.logFilePath = self.config.get("Settings", "logfilepath", fallback="C:/TimeLog.csv")
            self.timeout = self.config.getint("Settings", "timeout", fallback=10)
            self.useHeadless = self.config.getboolean("Settings", "useheadless", fallback=False)
        else:
            # Set default configuration values
            self.config["Mail-Setting"] = {"username":'', "password":'', "sender":'', "receiver":'', "smtpserver":'smtp.web.de'}  # typo corrected to "receiver"
            self.config["Account-Settings"] = {"usernameAttos":'', "pwAttos":''}
            self.config["Settings"] = {"timeout":10, "url": '', "isemailenabled": False, "iscsvenabled": True, "logfilepath": "C:/TimeLog.csv", "useheadless": False, "smtpport":587}

    def save_config(self):
        with open(self.config_ini_path, 'w') as configfile:
            self.config.write(configfile)

