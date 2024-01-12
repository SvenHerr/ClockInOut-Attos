import sqlite3
from datetime import datetime

class DbAccess:

    def __init__(self, db_path=':memory:'):
        self.conn = self.get_connection(db_path)
        self.cursor = self.conn.cursor()

    def get_connection(self, db_path):
        # Connect to the SQLite database (creates it if it doesn't exist)
        conn = sqlite3.connect(db_path)
        return conn

    def createDbIfNotExists(self):
        # Create a cursor object to interact with the database
        # Create a table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS times (
                Date DATETIME,
                StoredTime DATETIME,
                ExecutedTime DATETIME,
                Message TEXT,
                ErrorMessage TEXT
            )
        ''')

    def storeToDB(self, storedTime, message, error):
        #cursor = conn.cursor()

        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_date = datetime.now().strftime('%Y-%m-%d')

        # SQL query to insert values into the table
        sql = "INSERT INTO times (Date, StoredTime, ExecutedTime, Message, ErrorMessage) VALUES (?, ?, ?, ?, ?)"

        # Values to be inserted
        values = (current_date, storedTime, current_datetime, message, error)

        # Execute the query
        self.cursor.execute(sql, values)

        # Commit changes to the database
        self.conn.commit()

        # Close the cursor and the connection
        #cursor.close()
        #conn.close()

    def get_login_times(self, current_date):
        sql = "SELECT StoredTime, Message FROM times WHERE Date = ? AND (Message = 'Kommen' OR Message = 'Gehen') ORDER BY StoredTime"
        self.cursor.execute(sql, (current_date,))

        # Fetch all rows and calculate the total login time
        rows = self.cursor.fetchall()
        
        # Close the database connection
        self.conn.close()

        return rows