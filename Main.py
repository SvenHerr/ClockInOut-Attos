from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
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

# Check if the configuration file exists
if os.path.isfile(str(os.getcwd()) + "/timeclocker_config.ini"):
    config.read("timeclocker_config.ini")
    # Read configuration values
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
    # Set default configuration values
    config["Mail-Setting"] = {"username":'', "password":'', "sender":'', "reciever":'', "smtpserver":'smtp.web.de'}
    config["Account-Settings"] = {"usenameAttos":'', "pwAttos":''}
    config["Settings"] = {"timeout":10, "url": '', "isemailenabled": False, "iscsvenabled": True, "logfilepath": "C:/TimeLog.csv", "useheadless": False, "smtpport":587}
    
    # Write the default configuration to the file
    with open("timeclocker_config.ini", "w") as configfile:
        config.write(configfile)

errorNotFound = "Not found!"
exceptionNoInputElements = "No input elements found!"
exceptionNoArgsProvided = "No args provided!"
salden = "salden"
logout = "out"
login = "in"

# Wait until an element is visible on the page
def waitUnitElementIsVisible(by = By.ID, element = ''):
    """
    Waits until an element is visible on the page.

    Parameters:
        by (str): The locator strategy to use (default is By.ID).
        element (str): The locator value of the element to wait for (default is '').

    Returns:
        WebElement: The visible element on the page.
    """
    return WebDriverWait(browser, timeout).until(EC.presence_of_element_located((by, element)))

# Wait until multiple elements are visible on the page
def waitUnitElementsAreVisible(by = By.ID, elements = ''):
    """
    Waits until multiple elements are visible on the page.

    Parameters:
        by (str): The locator strategy to use (default is By.ID).
        elements (str): The locator value of the elements to wait for (default is '').

    Returns:
        List[WebElement]: A list of visible elements on the page.
    """
    return WebDriverWait(browser, timeout).until(EC.presence_of_all_elements_located((by, elements)))

# Retrieves a single element from the page.
def getElement(by = By.ID, element = ''):
    """
    Retrieves a single element from the page.

    Parameters:
        by (str): The locator strategy to use (default is By.ID).
        element (str): The locator value of the element to retrieve (default is '').

    Returns:
        WebElement: The retrieved element.

    Raises:
        Exception: If useHeadless is True and the element is not found.
    """
    if useHeadless == 'True':
        return browser.find_element(by, element)
    waitUnitElementIsVisible(by, element)

# Retrieves multiple elements from the page.
def getElements(by = By.ID, elements = ''):
    """
    Retrieves multiple elements from the page.

    Parameters:
        by (str): The locator strategy to use (default is By.ID).
        elements (str): The locator value of the elements to retrieve (default is '').

    Returns:
        List[WebElement]: A list of retrieved elements.

    Raises:
        Exception: If useHeadless is True and no elements are found.
    """
    if useHeadless == 'True':
        return browser.find_elements(by, elements)
    waitUnitElementsAreVisible(by, elements)

# Connect to the website using Selenium WebDriver
def connect():
    """
    Connects to the website using Selenium WebDriver.

    Global Variables:
        browser (WebDriver): The WebDriver instance for interacting with the website.

    Raises:
        WebDriverException: If an error occurs while setting up the WebDriver.
    """
    global browser
    #make headless for more convinient
    options = Options()
    if useHeadless == 'True':
        options.add_argument('--headless')
        # disable annoying logmessage if headless
        options.add_argument("--log-level=3") 
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
    try:
        browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        browser.get(url)
        browser.maximize_window()	
        browser.implicitly_wait(2)
    except WebDriverException as e:
        raise WebDriverException("Error occurred while setting up the WebDriver: " + str(e))

# Switch to the iframe containing the login form
def switchToIframe():
    """
    Switches the WebDriver focus to an iframe.

    Global Variables:
        browser (WebDriver): The WebDriver instance for interacting with the website.

    Raises:
        NoSuchElementException: If the iframe element is not found.
        WebDriverException: If an error occurs while switching to the iframe.
    """
    iframe_ref = getElement(By.TAG_NAME, 'iframe')
    browser.switch_to.frame(iframe_ref)

# Set the input elements on the page
def setInputElements():
    """
    Retrieves and stores all input elements on the webpage.

    Global Variables:
        inputElements (list): A list to store the input elements.
        exceptionNoInputElements (str): An exception message for when no input elements are found.

    Raises:
        Exception: If no input elements are found on the webpage.
    """
    global inputElements
    inputElements = getElements(By.TAG_NAME, 'input')
    if inputElements == None: 
        raise Exception(exceptionNoInputElements)

# Insert the account number into the input field
def insertAccoutNumber():
    """
    Inserts the account number into the first input element on the webpage.

    Global Variables:
        inputElements (list): A list containing input elements.
        usenameAttos (str): The account number to be inserted.

    Notes:
        - The account number is inserted into the first input element in the inputElements list.
        - The inputElements list should be populated before calling this function, typically by calling the setInputElements function.
    """
    inputElements[0].send_keys(usenameAttos)

# Insert the password into the input field
def insertPw():
    """
    Inserts the password into the second input element on the webpage.

    Global Variables:
        inputElements (list): A list containing input elements.
        pwAttos (str): The password to be inserted.

    Notes:
        - The password is inserted into the second input element in the inputElements list.
        - The inputElements list should be populated before calling this function, typically by calling the setInputElements function.
    """
    inputElements[1].send_keys(pwAttos)

# Set the select elements on the page
def setSelectElements():
    """
    Retrieves and stores the select elements from the webpage.

    Global Variables:
        selectedElements (list): A list containing select elements.

    Notes:
        - The select elements are retrieved by their tag name 'select' using the getElements function.
        - If no select elements are found, an exception (exceptionNoInputElements) is raised.
        - The selectedElements list is updated with the retrieved select elements.
    """
    global selectedElements
    selectedElements = getElements(By.TAG_NAME, 'select')
    if selectedElements == None: 
        raise Exception(exceptionNoInputElements)
    
# Set the booking type based on the command line argument
def setBookingTypeFromArgs():
    """
    Sets the booking type based on the command line argument.

    Global Variables:
        selectText (str): The text to be selected in the select element.

    Notes:
        - The booking type is determined based on the value of the 'call' command line argument.
        - If the 'call' argument is equal to 'login', the selectText is set to 'Kommen'.
        - If the 'call' argument is equal to 'logout', the selectText is set to 'Gehen'.
        - If the 'call' argument is neither 'login' nor 'logout', the selectText is set to an empty string.
    """
    global selectText
    if call == login:
        selectText = 'Kommen'
    elif call == logout:
        selectText = 'Gehen'
    else:
        selectText = ''

# Set the booking type in the select element
def setBookingType():
    """
    Sets the booking type in the select element.

    Global Variables:
        selectedElements (list): A list containing select elements.
        selectText (str): The text to be selected in the select element.

    Notes:
        - The select element to be updated is assumed to be the first element in the selectedElements list.
        - The select element is accessed using its index (0) in the selectedElements list.
        - The Select class from the selenium.webdriver.support.select module is used to interact with the select element.
        - The select.select_by_visible_text() method is used to select an option in the select element based on its visible text.
        - The selectText global variable contains the text to be selected in the select element.
    """
    select = Select(selectedElements[0])
    select.select_by_visible_text(selectText)

# Set the button elements on the page
def setButtonElements():
    """
    Retrieves and stores button elements from the webpage.

    Global Variables:
        buttonElements (list): A list containing button elements.

    Notes:
        - The button elements are retrieved using the browser's find_elements() method with the tag name 'button'.
        - The retrieved button elements are stored in the buttonElements global variable.
        - If the number of retrieved button elements is less than or equal to 1, an exception is raised (exceptionNoInputElements).
    """
    global buttonElements
    buttonElements = browser.find_elements(By.TAG_NAME, 'button')  
    if len(buttonElements) <= 1: 
        raise Exception(exceptionNoInputElements)

# Click the "Salden" button to view balance information
def clickSaldenButton():
    """
    Clicks the "Salden" button to view balance information.

    Notes:
        - The buttonElements global variable is assumed to contain the button elements retrieved from the webpage.
        - The button at index 1 is clicked using the ActionChains class from Selenium's webdriver.
    """
    ActionChains(browser).click(buttonElements[1]).perform()

# Click the "Accept" button to confirm the booking
def clickAcceptButton():
    """
    Clicks the "Accept" button to view balance information.

    Notes:
        - The buttonElements global variable is assumed to contain the button elements retrieved from the webpage.
        - The button at index 1 is clicked using the ActionChains class from Selenium's webdriver.
    """
    ActionChains(browser).click(buttonElements[0]).perform()

# Get the booked time from the page
def getBookedTime():
    """
    Retrieves the booked time from the webpage.

    Global Variables:
        actuallyBookedTime (str): The booked time.

    Notes:
        - The labelForVerbuchteZeit element is retrieved using the browser's find_element() method with the XPath provided.
        - The retrieved element's text content is stored in the actuallyBookedTime global variable.
        - If the labelForVerbuchteZeit element is not found, the actuallyBookedTime is set to errorNotFound.
    """
    labelForVerbuchteZeit = getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[1]/td/div/div/table/tbody/tr[5]/td[3]/div')
    
    global actuallyBookedTime
    if labelForVerbuchteZeit is not None:
        actuallyBookedTime = labelForVerbuchteZeit.text
    else:
        actuallyBookedTime = errorNotFound

# Get the label name for the flex time
def getFlexTimeLabelName():
    """
    Retrieves the label name for the flex time from the webpage.

    Returns:
        str: The label name for the flex time.

    Notes:
        - The flexTimeLabel element is retrieved using the browser's find_element() method with the XPath provided.
        - If the flexTimeLabel element is found, its text content is returned.
        - If the flexTimeLabel element is not found, the errorNotFound string is returned.
    """
    flexTimeLabel = getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[1]/td[3]/div/span')
    if flexTimeLabel is not None:
        return flexTimeLabel.text
    return errorNotFound

# Get the flex time from the page
def getFlexTime():
    """
    Retrieves the flex time from the webpage.

    Returns:
        str: The flex time.

    Notes:
        - The labelForFlexTime element is retrieved using the browser's find_element() method with the XPath provided.
        - If the labelForFlexTime element is found, its text content is returned.
        - If the labelForFlexTime element is not found, the errorNotFound string is returned.
    """
    labelForFlexTime = getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[1]/td[5]/div/span')
    if labelForFlexTime is not None:
        return labelForFlexTime.text
    return errorNotFound

# Get the label name for the vacation days
def getVacationDaysLabelName():
    """
    Retrieves the label name for the vacation days from the webpage.

    Returns:
        str: The label name for the vacation days.

    Notes:
        - The vacationDaysLabel element is retrieved using the browser's find_element() method with the XPath provided.
        - If the vacationDaysLabel element is found, its text content is returned.
        - If the vacationDaysLabel element is not found, the errorNotFound string is returned.
    """
    vacationDaysLabel = getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[3]/td[3]/div/span')
    if vacationDaysLabel is not None:
        return vacationDaysLabel.text
    return errorNotFound

# Get the vacation days from the page
def getVacationDays():
    """
    Retrieves the vacation days from the webpage.

    Returns:
        str: The vacation days.

    Notes:
        - The labelForVacationDays element is retrieved using the browser's find_element() method with the XPath provided.
        - If the labelForVacationDays element is found, its text content is returned.
        - If the labelForVacationDays element is not found, the errorNotFound string is returned.
    """
    labelForVacationDays = getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[3]/td[5]/div/span')
    if labelForVacationDays is not None:
        return labelForVacationDays.text
    return errorNotFound

# Get the label name for the old vacation days
def getOldVacationDaysLabelName():
    """
    Retrieves the label name for the old vacation days from the webpage.

    Returns:
        str: The label name for the old vacation days.

    Notes:
        - The oldVacationDaysLabel element is retrieved using the browser's find_element() method with the XPath provided.
        - If the oldVacationDaysLabel element is found, its text content is returned.
        - If the oldVacationDaysLabel element is not found, the errorNotFound string is returned.
    """
    oldVacationDaysLabel = getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[5]/td[3]/div/span')
    if oldVacationDaysLabel is not None:
        return oldVacationDaysLabel.text
    return errorNotFound

# Get the old vacation days from the page
def getOldVacationDays():
    """
    Retrieves the old vacation days from the webpage.

    Returns:
        str: The old vacation days.

    Notes:
        - The labelForOldVacationDays element is retrieved using the browser's find_element() method with the XPath provided.
        - If the labelForOldVacationDays element is found, its text content is returned.
        - If the labelForOldVacationDays element is not found, the errorNotFound string is returned.
    """
    labelForOldVacationDays = getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[5]/td[5]/div/span')
    if labelForOldVacationDays is not None:
        return labelForOldVacationDays.text
    return errorNotFound

# Check if the log file already exists
def fileExists():
    """
    Checks if a file exists at the specified logFilePath.

    Returns:
        bool: True if the file exists, False otherwise.

    Notes:
        - The os.path.exists() method is used to check if a file exists at the specified logFilePath.
        - Returns True if the file exists, and False otherwise.
    """
    fileExists = os.path.exists(logFilePath)
    return fileExists

# Store the booked time to a CSV file
def storeTimeToCSV():
    """
    Stores the booked time to a CSV file.

    Global Variables:
        dateToday (datetime): The current date.

    Notes:
        - The dateToday global variable is set to the current date using datetime.today().
        - The data list is created with the values: [dateToday, selectText, actuallyBookedTime].
        - The CSV file at logFilePath is opened in 'a' (append) mode with UTF8 encoding.
        - If the fileExists() function returns False, a header list is created with the column names.
        - The data list is written to the CSV file using csv.writer.writerow() method.
    """
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

# Quit the browser session
def quit():
    """
    Quits the browser instance.

    Notes:
        - The browser instance is closed using the browser.quit() method.
    """
    browser.quit()

# Send an email
def sendMail(subject, body):
    """
    Sends an email with the specified subject and body.

    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.

    Notes:
        - The email is sent using the SMTP protocol.
        - The email is sent from the 'sender' to the 'receiver' with the specified subject and body.
        - The email server requires authentication using the 'username' and 'password'.
        - The email is sent using the 'smtpServer' and 'smtpPort'.
        - Debug information is printed for troubleshooting purposes.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = reciever
    part = MIMEText(body, 'plain')
    msg.attach(part)

    # Create a Mail Session
    smtpObj = smtplib.SMTP(smtpServer, smtpPort)
    # Print debug information
    smtpObj.set_debuglevel(1)
    # If the server requires authentication
    smtpObj.starttls()
    smtpObj.login(username, password)
    # Send the email
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
            #body = selectText + "actually booked time: "+ actuallyBookedTime + ". Should have booked time: " + str(dateToday)
            body = f"{selectText} actually booked time: {actuallyBookedTime}. Should have booked time: {dateToday}"
            sendMail(subject, body)
    except Exception as ex:
        if isEmailEnabled == 'True':
            sendMail("Time not booked!","Error:" + str(ex))
        print(ex)
        exit(1)

    quit()
    exit(0)