import smtplib
from email.message import EmailMessage
import random
from credentials import *

def email_verification():
    code = ""
    for i in range(6):
        code += str(random.randint(0,9))

    msg = EmailMessage()
    msg.set_content("Your verification code is " + code)

    msg['Subject'] = "Study Buddy email verification"
    msg['From'] = "devsb1234567890@gmail.com"
    msg['To'] = "zheliha02@gmail.com"

    password = GM_PASSWORD

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("devsb1234567890@gmail.com", password)
    server.send_message(msg)
    server.quit()

    return code
