from datetime import datetime
import csv  

# Store the booked time to a CSV file
def storeTimeToCSV(self, date, selectText, actuallyBookedTime):
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

    with open(self.logFilePath, 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
            
        if self.fileExists() == False:
            header = ['Booked Time', 'Status', 'Actually booked Time', ]
            # write the header
            writer.writerow(header)
        # write the data
        writer.writerow(data)