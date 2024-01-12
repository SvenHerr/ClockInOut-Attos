from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver

class BrowserHandler:

    errorNotFound = "Not found!"
    exceptionNoInputElements = "No input elements found!"
    exceptionNoArgsProvided = "No args provided!"
    salden = "salden"
    time_today = "time"
    time_for = "time-for"
    logout = "out"
    login = "in"
    

    def __init__(self, config):
        # This is the constructor
        self.config = config
        self.browser = None  # Initialize browser as an instance variable

    # Wait until an element is visible on the page
    def waitUnitElementIsVisible(self, by = By.ID, element = ''):
        """
        Waits until an element is visible on the page.

        Parameters:
            by (str): The locator strategy to use (default is By.ID).
            element (str): The locator value of the element to wait for (default is '').

        Returns:
            WebElement: The visible element on the page.
        """
    
        print(f"Waiting for element with locator {by} and value {element} to be visible...")
        return WebDriverWait(self.browser, self.config.timeout).until(EC.presence_of_element_located((by, element)))


    # Wait until multiple elements are visible on the page
    def waitUnitElementsAreVisible(self, by = By.ID, elements = ''):
        """
        Waits until multiple elements are visible on the page.

        Parameters:
            by (str): The locator strategy to use (default is By.ID).
            elements (str): The locator value of the elements to wait for (default is '').

        Returns:
            List[WebElement]: A list of visible elements on the page.
        """

        print(f"Waiting for element with locator {by} and value {elements} to be visible...")
        return WebDriverWait(self.browser, self.config.timeout).until(EC.presence_of_all_elements_located((by, elements)))
    

    # Retrieves a single element from the page.
    def getElement(self, by = By.ID, element = ''):
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
        if self.config.useHeadless == 'True':
            return self.browser.find_element(by, element)
        self.waitUnitElementIsVisible(by, element)
        print(f"Finished for element with locator {by} and value {element} is visible!")

    # Retrieves multiple elements from the page.
    def getElements(self, by = By.ID, elements = ''):
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
        if self.config.useHeadless == 'True':
            return self.browser.find_elements(by, elements)
        self.waitUnitElementsAreVisible(by, elements)
        print("Visible")

    # Connect to the website using Selenium WebDriver
    def connect(self):
        """
        Connects to the website using Selenium WebDriver.

        Raises:
            WebDriverException: If an error occurs while setting up the WebDriver.
        """
        options = Options()
        if self.config.useHeadless == 'True':
            options.add_argument('--headless')
            options.add_argument("--log-level=3")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
        try:
            self.browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
            self.browser.get(self.config.url)
            self.browser.maximize_window()
            self.browser.implicitly_wait(2)
        except WebDriverException as e:
            raise WebDriverException("Error occurred while setting up the WebDriver: " + str(e))

    # Switch to the iframe containing the login form
    def switchToIframe(self):
        """
        Switches the WebDriver focus to an iframe.

        Global Variables:
            browser (WebDriver): The WebDriver instance for interacting with the website.

        Raises:
            NoSuchElementException: If the iframe element is not found.
            WebDriverException: If an error occurs while switching to the iframe.
        """
        iframe_ref = self.getElement(By.TAG_NAME, 'iframe')
        self.browser.switch_to.frame(iframe_ref)

    # Set the input elements on the page
    def setInputElements(self):
        """
        Retrieves and stores all input elements on the webpage.

        Global Variables:
            inputElements (list): A list to store the input elements.
            exceptionNoInputElements (str): An exception message for when no input elements are found.

        Raises:
            Exception: If no input elements are found on the webpage.
        """
        global inputElements
        inputElements = self.getElements(By.TAG_NAME, 'input')
        if inputElements == None: 
            raise Exception(self.exceptionNoInputElements)

    # Insert the account number into the input field
    def insertAccoutNumber(self):
        """
        Inserts the account number into the first input element on the webpage.

        Global Variables:
            inputElements (list): A list containing input elements.
            usenameAttos (str): The account number to be inserted.

        Notes:
            - The account number is inserted into the first input element in the inputElements list.
            - The inputElements list should be populated before calling this function, typically by calling the setInputElements function.
        """
        inputElements[0].send_keys(self.config.usenameAttos)

    # Insert the password into the input field
    def insertPw(self):
        """
        Inserts the password into the second input element on the webpage.

        Global Variables:
            inputElements (list): A list containing input elements.
            pwAttos (str): The password to be inserted.

        Notes:
            - The password is inserted into the second input element in the inputElements list.
            - The inputElements list should be populated before calling this function, typically by calling the setInputElements function.
        """
        inputElements[1].send_keys(self.config.pwAttos)

    # Set the select elements on the page
    def setSelectElements(self):
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
        selectedElements = self.getElements(By.TAG_NAME, 'select')
        if selectedElements == None: 
            raise Exception(self.exceptionNoInputElements)

    selectText = ''
    # Set the booking type based on the command line argument
    def setBookingTypeFromArgs(self):
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
        if self.call == self.login:
            selectText = 'Kommen'
        elif self.call == self.logout:
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
    def setButtonElements(self):
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
        buttonElements = self.browser.find_elements(By.TAG_NAME, 'button')  
        if len(buttonElements) <= 1: 
            raise Exception(self.exceptionNoInputElements)

    # Click the "Salden" button to view balance information
    def clickSaldenButton(self):
        """
        Clicks the "Salden" button to view balance information.

        Notes:
            - The buttonElements global variable is assumed to contain the button elements retrieved from the webpage.
            - The button at index 1 is clicked using the ActionChains class from Selenium's webdriver.
        """
        ActionChains(self.browser).click(buttonElements[1]).perform()

    # Click the "Accept" button to confirm the booking
    def clickAcceptButton(self):
        """
        Clicks the "Accept" button to view balance information.

        Notes:
            - The buttonElements global variable is assumed to contain the button elements retrieved from the webpage.
            - The button at index 1 is clicked using the ActionChains class from Selenium's webdriver.
        """
        ActionChains(self.browser).click(buttonElements[0]).perform()

    # Get the booked time from the page
    def getBookedTime(self):
        """
        Retrieves the booked time from the webpage.

        Global Variables:
            actuallyBookedTime (str): The booked time.

        Notes:
            - The labelForVerbuchteZeit element is retrieved using the browser's find_element() method with the XPath provided.
            - The retrieved element's text content is stored in the actuallyBookedTime global variable.
            - If the labelForVerbuchteZeit element is not found, the actuallyBookedTime is set to errorNotFound.
        """
        labelForVerbuchteZeit = self.getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[1]/td/div/div/table/tbody/tr[5]/td[3]/div')
        
        global actuallyBookedTime
        if labelForVerbuchteZeit is not None:
            actuallyBookedTime = labelForVerbuchteZeit.text
        else:
            actuallyBookedTime = self.errorNotFound

    # Get the label name for the flex time
    def getFlexTimeLabelName(self):
        """
        Retrieves the label name for the flex time from the webpage.

        Returns:
            str: The label name for the flex time.

        Notes:
            - The flexTimeLabel element is retrieved using the browser's find_element() method with the XPath provided.
            - If the flexTimeLabel element is found, its text content is returned.
            - If the flexTimeLabel element is not found, the errorNotFound string is returned.
        """
        flexTimeLabel = self.getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[1]/td[3]/div/span')
        if flexTimeLabel is not None:
            return flexTimeLabel.text
        return self.errorNotFound

    # Get the flex time from the page
    def getFlexTime(self):
        """
        Retrieves the flex time from the webpage.

        Returns:
            str: The flex time.

        Notes:
            - The labelForFlexTime element is retrieved using the browser's find_element() method with the XPath provided.
            - If the labelForFlexTime element is found, its text content is returned.
            - If the labelForFlexTime element is not found, the errorNotFound string is returned.
        """
        labelForFlexTime = self.getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[1]/td[5]/div/span')
        if labelForFlexTime is not None:
            return labelForFlexTime.text
        return self.errorNotFound

    # Get the label name for the vacation days
    def getVacationDaysLabelName(self):
        """
        Retrieves the label name for the vacation days from the webpage.

        Returns:
            str: The label name for the vacation days.

        Notes:
            - The vacationDaysLabel element is retrieved using the browser's find_element() method with the XPath provided.
            - If the vacationDaysLabel element is found, its text content is returned.
            - If the vacationDaysLabel element is not found, the errorNotFound string is returned.
        """
        vacationDaysLabel = self.getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[3]/td[3]/div/span')
        if vacationDaysLabel is not None:
            return vacationDaysLabel.text
        return self.errorNotFound

    # Get the vacation days from the page
    def getVacationDays(self):
        """
        Retrieves the vacation days from the webpage.

        Returns:
            str: The vacation days.

        Notes:
            - The labelForVacationDays element is retrieved using the browser's find_element() method with the XPath provided.
            - If the labelForVacationDays element is found, its text content is returned.
            - If the labelForVacationDays element is not found, the errorNotFound string is returned.
        """
        labelForVacationDays = self.getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[3]/td[5]/div/span')
        if labelForVacationDays is not None:
            return labelForVacationDays.text
        return self.errorNotFound

    # Get the label name for the old vacation days
    def getOldVacationDaysLabelName(self):
        """
        Retrieves the label name for the old vacation days from the webpage.

        Returns:
            str: The label name for the old vacation days.

        Notes:
            - The oldVacationDaysLabel element is retrieved using the browser's find_element() method with the XPath provided.
            - If the oldVacationDaysLabel element is found, its text content is returned.
            - If the oldVacationDaysLabel element is not found, the errorNotFound string is returned.
        """
        oldVacationDaysLabel = self.getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[5]/td[3]/div/span')
        if oldVacationDaysLabel is not None:
            return oldVacationDaysLabel.text
        return self.errorNotFound

    # Get the old vacation days from the page
    def getOldVacationDays(self):
        """
        Retrieves the old vacation days from the webpage.

        Returns:
            str: The old vacation days.

        Notes:
            - The labelForOldVacationDays element is retrieved using the browser's find_element() method with the XPath provided.
            - If the labelForOldVacationDays element is found, its text content is returned.
            - If the labelForOldVacationDays element is not found, the errorNotFound string is returned.
        """
        labelForOldVacationDays = self.getElement(By.XPATH, '/html/body/div/form/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[5]/td/div/div/table/tbody/tr[5]/td[5]/div/span')
        if labelForOldVacationDays is not None:
            return labelForOldVacationDays.text
        return self.errorNotFound

    
    # Quit the browser session
    def quit(self):
        """
        Quits the browser instance.

        Notes:
            - The browser instance is closed using the browser.quit() method.
        """
        self.browser.quit()



# from ConfigClass import ConfigClass

# config_ini_path = "timeclocker_config.ini"
# config = ConfigClass(config_ini_path)
# test = BrowserHandler(config)
# test.connect()