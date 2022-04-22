import datetime
import os
from datetime import date
from dateutil.relativedelta import relativedelta
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from dotenv import load_dotenv


def clean_datetime(val):
    try:
        val = val.strip()
        datepart, timepart = val.split(" ")
        print(datepart)
        print(timepart)
        year, month, day = map(int, datepart.split("-"))
        # hours, minutes, seconds = map(int, timepart.split(":"))
        timelist = timepart.split(":")

        hours, minutes, seconds, microseconds = 0, 0, 0, 0 
        if len(timelist) == 3:
            hours, minutes, seconds = map(int, timepart.split(":"))
        elif len(timelist) == 2:
            hours, minutes = map(int, timepart.split(":"))
        elif len(timelist) == 1:
            hours = map(int, timepart.split(":"))

        val = datetime.datetime(year, month, day, hours, minutes, seconds, microseconds)
        return f"{val:%Y-%m-%d %H:%M:%S}"

    except Exception as e:
        return None



load_dotenv()


# SEND SMS
proxy_client = TwilioHttpClient(proxy={'http': os.getenv("http_proxy"), 'https': os.getenv("https_proxy")})
twilio_client = Client(http_client=proxy_client)

def send_sms_reminder(reminder):
    twilio_from = os.getenv("TWILIO_SMS_FROM")
    to_phone_number = reminder['phone_number']
    message = 'Hello, Here is {} Reminder for you: {}.'.format(reminder['name'], reminder['description'])
    twilio_client.messages.create(
        body=message,
        from_=f"{twilio_from}",
        to=f"{to_phone_number}"
    )


# SEND EMAIL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
PORT = os.getenv("SMTP_PORT")


def send_email(reminder):
    # Send TEXT Mime Email
    email = reminder['email']
    email_body = 'Hello, Here is {} Reminder for you: {}.'.format(reminder['name'], reminder['description'])

    smtp_server = SMTP_SERVER
    port = PORT
    sender_email = EMAIL
    password = EMAIL_PASSWORD

    message = MIMEMultipart("alternative")
    message["Subject"] = 'REMINDER: {}'.format(reminder['name'])
    message["From"] = sender_email
    message["To"] = reminder['email']

    # Turn these into plain MIMEText objects
    part1 = MIMEText(email_body, "plain")

    # Add plain-text parts to MIMEMultipart message
    message.attach(part1)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        # Send email
        server.sendmail(sender_email, email, message.as_string())
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        return {'errors': e}
    finally:
        server.quit()




from flask_apscheduler import APScheduler

scheduler = APScheduler()

