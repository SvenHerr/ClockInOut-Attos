from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from email.mime.multipart import MIMEMultipart
from selenium.webdriver import ActionChains
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from email.mime.text import MIMEText
from selenium import webdriver
from datetime import datetime
from datetime import date
import configparser
import smtplib
import sys
import csv  
import os

# First create config if not exist
config = configparser.ConfigParser()
if os.path.isfile(str(os.getcwd()) + "/timeclocker_config.ini"):
    config.read("timeclocker_config.ini")
    username = config["Mail-Setting"]["username"]
    password = config["Mail-Setting"]["password"]
    sender = config["Mail-Setting"]["sender"]
    reciever = config["Mail-Setting"]["reciever"]
    smtpServer = config["Mail-Setting"]["smtpserver"]
    smtpPort = config["Mail-Setting"]["smtpport"]
    usenameAttos = config["Account-Settings"]["usernameAttos"]
    pwAttos = config["Account-Settings"]["pwAttos"]
    url = config["Settings"]["url"]
    isEmailEnabled = config["Settings"]["isemailenabled"]
    isCSVEnabled = config["Settings"]["iscsvenabled"]
    logFilePath = config["Settings"]["logfilepath"]
    timeout = config["Settings"]["timeout"]
    useHeadless = config["Settings"]["useheadless"]
else:
    config["Mail-Setting"] = {"username":'', "password":'', "sender":'', "reciever":'', "smtpserver":'smtp.web.de'}
    config["Account-Settings"] = {"usenameAttos":'', "pwAttos":''}
    config["Settings"] = {"timeout":10, "url": '', "isemailenabled": False, "iscsvenabled": True, "logfilepath": "C:/TimeLog.csv", "useheadless": False, "smtpport":587}
    with open("timeclocker_config.ini", "w") as configfile:
        config.write(configfile)


def waitUnitElementIsVisible(by = By.ID, element = ''):
    return WebDriverWait(browser, timeout).until(EC.presence_of_element_located((by, element)))

def connect():
    global browser
    #make headless for more convinient
    if useHeadless:
        options = Options()
        options.add_argument('--headless')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.get(url)
    browser.maximize_window()	
    browser.implicitly_wait(2)

def switchToIframe():
    iframe_ref = waitUnitElementIsVisible(By.TAG_NAME, 'iframe')
    browser.switch_to.frame(iframe_ref)

def getInputElements():
    global inputElements
    inputElements = waitUnitElementIsVisible(By.TAG_NAME, 'input')
    if len(inputElements) <= 1: 
        raise Exception("No input elements found!")

def insertAccoutNumber():
    inputElements[0].send_keys(usenameAttos)

def insertPw():
    inputElements[1].send_keys(pwAttos)

def setSelectElements():
    global selectedElements
    selectedElements = waitUnitElementIsVisible(By.TAG_NAME, 'select')
    if selectedElements == None: 
        raise Exception("No input elements found!")

def setBookingTypeFromArgs():
    global selectText
    if call == 'in':
        selectText = 'Kommen'
    elif call == 'out':
        selectText = 'Gehen'
    else:
        selectText = ''

def setBookingType():
    select = Select(selectedElements[0])
    select.select_by_visible_text(selectText)

def setButtonElements():
    global buttonElements
    buttonElements = browser.find_elements(By.TAG_NAME, 'button')  
    if len(buttonElements) <= 1: 
        raise Exception("No input elements found!")

def clickSaldenButton():
    ActionChains(browser).click(buttonElements[1]).perform()

def clickAcceptButton():
    ActionChains(browser).click(buttonElements[0]).perform()

def getBookedTime():
    browser.implicitly_wait(2)
    labelForVerbuchteZeit = waitUnitElementIsVisible(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[1]/td/div/div/table/tbody/tr[5]/td[3]/div')
    
    global actuallyBookedTime
    if labelForVerbuchteZeit is not None:
        actuallyBookedTime = labelForVerbuchteZeit.text
    else:
        actuallyBookedTime ='error'

def storeTimeToCSV():
    global now
    now = datetime.now()
    header = ['Status', 'Actually booked Time', 'Booked Time']
    data = [selectText, actuallyBookedTime, now]

    with open(logFilePath, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        # write the data
        writer.writerow(data)

def quit():
    browser.switch_to.default_content()
    browser.quit()

def sendMail(subject, body):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = reciever
    part = MIMEText(body, 'plain')
    msg.attach(part)

    # Erzeugen einer Mail Session
    smtpObj = smtplib.SMTP(smtpServer, smtpPort)
    # Debuginformationen auf der Konsole ausgeben
    smtpObj.set_debuglevel(1)
    # Wenn der Server eine Authentifizierung benötigt dann...
    smtpObj.starttls()
    smtpObj.login(username, password)
    # absenden der E-Mail
    smtpObj.sendmail(sender, reciever, msg.as_string())



# Main
if __name__ == '__main__':

    try:
        if len(sys.argv) > 1:
            global call
            call = sys.argv[1]
    except Exception as ex:
        print(ex)
        exit(1)

    try:
        browser = connect()
        switchToIframe()
        elements = getInputElements()
        insertAccoutNumber()
        insertPw()
        setSelectElements()
        setBookingTypeFromArgs()
        setBookingType()
        setButtonElements()

        if call == 'salden':
            clickSaldenButton()
        elif call == 'out' or call == 'in':
            clickAcceptButton()
        else: 
            raise ValueError('No args')
        
        if isCSVEnabled:
            getBookedTime()
            storeTimeToCSV()

        subject = "Time booked!"
        body = selectText + "actually booked time: "+ actuallyBookedTime + ". Should have booked time: " + str(now)

        if isEmailEnabled == 'True':
            sendMail(subject, body)
    except Exception as ex:
        if isEmailEnabled == 'True':
            sendMail("Time not booked!","Error:" + str(ex))
        print(ex)
        exit(1)

    quit()
