import smtplib
from email.message import EmailMessage
import random
from credentials import *


def email_verification(recipient_email):
    code = ""
    for i in range(6):
        code += str(random.randint(0, 9))

    print(code)

    msg = EmailMessage()
    msg.set_content("Thank you for using Study Buddy! Your email verification code is " +
                    code + ". Kindly key this verification code back in Telegram to verify your account.")

    msg['Subject'] = "Study Buddy Email Verification"
    msg['From'] = GM_EMAIL
    msg['To'] = recipient_email

    password = GM_PASSWORD
    port = 465

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', port)
    server.login(GM_EMAIL, password)
    server.send_message(msg)
    server.quit()

    return code
