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

errorNotFound = "Not found!"
exceptionNoInputElements = "No input elements found!"
exceptionNoArgsProvided = "No args provided!"
salden = "salden"
logout = "out"
login = "in"

def waitUnitElementIsVisible(by = By.ID, element = ''):
    return WebDriverWait(browser, timeout).until(EC.presence_of_element_located((by, element)))

def waitUnitElementsAreVisible(by = By.ID, elements = ''):
    return WebDriverWait(browser, timeout).until(EC.presence_of_all_elements_located((by, elements)))

def connect():
    global browser
    #make headless for more convinient
    options = Options()
    if useHeadless == 'True':
        options.add_argument('--headless')
        # disable annoying logmessage if headless
        options.add_argument("--log-level=3") 
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    browser.get(url)
    browser.maximize_window()	
    browser.implicitly_wait(2)

def switchToIframe():
    iframe_ref = waitUnitElementIsVisible(By.TAG_NAME, 'iframe')
    browser.switch_to.frame(iframe_ref)

def setInputElements():
    global inputElements
    inputElements = waitUnitElementsAreVisible(By.TAG_NAME, 'input')
    if inputElements == None: 
        raise Exception(exceptionNoInputElements)

def insertAccoutNumber():
    inputElements[0].send_keys(usenameAttos)

def insertPw():
    inputElements[1].send_keys(pwAttos)

def setSelectElements():
    global selectedElements
    selectedElements = waitUnitElementsAreVisible(By.TAG_NAME, 'select')
    if selectedElements == None: 
        raise Exception(exceptionNoInputElements)

def setBookingTypeFromArgs():
    global selectText
    if call == login:
        selectText = 'Kommen'
    elif call == logout:
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
        raise Exception(exceptionNoInputElements)

def clickSaldenButton():
    ActionChains(browser).click(buttonElements[1]).perform()

def clickAcceptButton():
    ActionChains(browser).click(buttonElements[0]).perform()

def getBookedTime():
    labelForVerbuchteZeit = waitUnitElementIsVisible(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[1]/td/div/div/table/tbody/tr[5]/td[3]/div')
    
    global actuallyBookedTime
    if labelForVerbuchteZeit is not None:
        actuallyBookedTime = labelForVerbuchteZeit.text
    else:
        actuallyBookedTime = errorNotFound

def getFlexTimeLabelName():
    flexTimeLabel = waitUnitElementIsVisible(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[1]/td[3]/div/span')
    if flexTimeLabel is not None:
        return flexTimeLabel.text
    return errorNotFound

def getFlexTime():
    labelForFlexTime = waitUnitElementIsVisible(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[1]/td[5]/div/span')
    if labelForFlexTime is not None:
        return labelForFlexTime.text
    return errorNotFound

def getVacationDaysLabelName():
    vacationDaysLabel = waitUnitElementIsVisible(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[3]/td[3]/div/span')
    if vacationDaysLabel is not None:
        return vacationDaysLabel.text
    return errorNotFound

def getVacationDays():
    labelForVacationDays = waitUnitElementIsVisible(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[3]/td[5]/div/span')
    if labelForVacationDays is not None:
        return labelForVacationDays.text
    return errorNotFound

def getOldVacationDaysLabelName():
    oldVacationDaysLabel = waitUnitElementIsVisible(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[5]/td[3]/div/span')
    if oldVacationDaysLabel is not None:
        return oldVacationDaysLabel.text
    return errorNotFound

def getOldVacationDays():
    labelForOldVacationDays = waitUnitElementIsVisible(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[5]/td[5]/div/span')
    if labelForOldVacationDays is not None:
        return labelForOldVacationDays.text
    return errorNotFound

def fileExists():
    fileExists = os.path.exists(logFilePath)
    return fileExists

def storeTimeToCSV():
    global dateToday
    dateToday = datetime.today()
    data = [date, selectText, actuallyBookedTime]

    with open(logFilePath, 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        
        if fileExists() == False:
            header = ['Booked Time', 'Status', 'Actually booked Time', ]
            # write the header
            writer.writerow(header)
        # write the data
        writer.writerow(data)

def quit():
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
        else:
            call =""
            raise Exception(exceptionNoArgsProvided)
    except Exception as ex:
        print(ex)
        exit(1)

    try:
        connect()
        switchToIframe()
        setInputElements()
        insertAccoutNumber()
        insertPw()
        setSelectElements()
        setBookingTypeFromArgs()
        setBookingType()
        setButtonElements()

        if call == salden:
            clickSaldenButton()
            print(getFlexTimeLabelName() + " " + getFlexTime())
            print(getVacationDaysLabelName() + " " + getVacationDays())
            print(getOldVacationDaysLabelName() + " " + getOldVacationDays())
        elif call == logout or call == login:
            clickAcceptButton()
        else: 
            raise ValueError(exceptionNoArgsProvided)
        
        getBookedTime()
        print('Booked time:', actuallyBookedTime)
        if isCSVEnabled == 'True':
            storeTimeToCSV()        

        if isEmailEnabled == 'True':
            subject = "Time booked!"
            body = selectText + "actually booked time: "+ actuallyBookedTime + ". Should have booked time: " + str(dateToday)
            sendMail(subject, body)
    except Exception as ex:
        if isEmailEnabled == 'True':
            sendMail("Time not booked!","Error:" + str(ex))
        print(ex)
        exit(1)

    quit()
    exit(0)