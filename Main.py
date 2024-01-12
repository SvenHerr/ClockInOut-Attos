from datetime import datetime
import configparser
import sys

# custom imports
from DbHelper.DbAccess import get_login_times, get_connection
from Converter.timeConverter import seconds_to_hms
from BrowserHandler import BrowserHandler
from ConfigClass import ConfigClass

# First create config if not exist
config = configparser.ConfigParser()

def calculate_total_login_time(current_date):
    #current_date = '2024-01-09'  # Uncomment this line if you want to use a static date   

    rows = get_login_times(current_date)
    total_login_time = 0
    login_start_time = None

    if len(rows) == 1:
        print("Only login found in db")
        current_time = datetime.now().strftime("%H:%M:%S")
        current_time = datetime.strptime(current_time, "%H:%M:%S")
        current_time_seconds = current_time.hour * 3600 + current_time.minute * 60 + current_time.second
        row = rows[0]
        time_object = datetime.strptime(row[0], "%H:%M:%S")
        total_seconds = time_object.hour * 3600 + time_object.minute * 60 + time_object.second
        total_login_time = (current_time_seconds - total_seconds)
    else:
        for row in rows:
            stored_time = datetime.strptime(row[0], "%H:%M:%S")

            if row[1] == 'Kommen':
                login_start_time = stored_time
            elif row[1] == 'Gehen' and login_start_time:
                login_duration = (stored_time - login_start_time).total_seconds()
                total_login_time += login_duration
                login_start_time = None

    # Return the total login time in seconds
    return total_login_time


# Check if the configuration file exists
config_ini_path = "timeclocker_config.ini"
config = ConfigClass(config_ini_path)


errorNotFound = "Not found!"
exceptionNoInputElements = "No input elements found!"
exceptionNoArgsProvided = "No args provided!"
salden = "salden"
time_today = "time"
time_for = "time-for"
logout = "out"
login = "in"




# Main
if __name__ == '__main__':

    browserHandler = BrowserHandler(config)
    browserHandler.connect()
    browserHandler.switchToIframe()
    browserHandler.setInputElements()
    browserHandler.insertAccoutNumber()
    browserHandler.insertPw()
    browserHandler.setSelectElements()
    browserHandler.setBookingTypeFromArgs()
    browserHandler.setBookingType()
    browserHandler.setButtonElements()

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
        get_connection()
    except Exception as ex:
        print(ex)
        
    if call == time_today:
        current_date = datetime.now().strftime('%Y-%m-%d')
        total_login_time = calculate_total_login_time(current_date)
        # Convert total login time to hours, minutes, and seconds
        hours, minutes, seconds = seconds_to_hms(total_login_time)
        print(f"You worked: {hours}h {minutes}m")
        exit(0)

    try:
        browserHandler = BrowserHandler(config)
        browserHandler.connect()
        browserHandler.switchToIframe()
        browserHandler.setInputElements()
        browserHandler.insertAccoutNumber()
        browserHandler.insertPw()
        browserHandler.setSelectElements()
        browserHandler.setBookingTypeFromArgs()
        browserHandler.setBookingType()
        browserHandler.setButtonElements()

        if call == salden:
            browserHandler.clickSaldenButton()
            print(browserHandler.getFlexTimeLabelName() + " " + browserHandler.getFlexTime())
            print(browserHandler.getVacationDaysLabelName() + " " + browserHandler.getVacationDays())
            print(browserHandler.getOldVacationDaysLabelName() + " " + browserHandler.getOldVacationDays())
        elif call == logout or call == login:
            browserHandler.clickAcceptButton()
        else: 
            raise ValueError(exceptionNoArgsProvided)
        
        browserHandler.getBookedTime()
        print('Booked time:', browserHandler.actuallyBookedTime)
        if config.isCSVEnabled == 'True':
            browserHandler.storeTimeToCSV()        

        if config.isEmailEnabled == 'True':
            subject = "Time booked!"
            #body = selectText + "actually booked time: "+ actuallyBookedTime + ". Should have booked time: " + str(dateToday)
            body = f"{browserHandler.selectText} actually booked time: {browserHandler.actuallyBookedTime}. Should have booked time: {browserHandler.dateToday}"
            browserHandler.sendMail(subject, body)
    except Exception as ex:
        if config.isEmailEnabled == 'True':
            browserHandler.sendMail("Time not booked!","Error:" + str(ex))
        print(ex)
        browserHandler.storeToDB(browserHandler.actuallyBookedTime,browserHandler.selectText,ex)
        browserHandler.cursor.close()
        browserHandler.conn.close()
        exit(1)

    browserHandler.storeToDB(browserHandler.actuallyBookedTime,browserHandler.selectText,None)

    browserHandler.cursor.close()
    browserHandler.conn.close()
    browserHandler.quit()
    exit(0)