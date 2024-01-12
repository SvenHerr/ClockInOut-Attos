import os

# Check if the log file already exists
def fileExists(self):
    """
    Checks if a file exists at the specified logFilePath.

    Returns:
        bool: True if the file exists, False otherwise.

    Notes:
        - The os.path.exists() method is used to check if a file exists at the specified logFilePath.
        - Returns True if the file exists, and False otherwise.
    """
    fileExists = os.path.exists(self.logFilePath)
    return fileExists