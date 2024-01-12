from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Send an email
def sendMail(subject, body, sender, reciever, smtpServer, smtpPort, username, password):
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