# Reminder App
Build an Email and SMS Reminder Service using Flask 2.0 and APScheduler python


## Operations
- create user 
- login 

- create reminder
- update reminder
- delete reminder
- repeat reminder (Daily, Weekly, Monthly, Yearly)

- view all reminder
- view calender and reminder
- view specific reminder

- reminder notification
	1. send SMS Notification
    2. send Email Notification

## Requirements
- python 3.8
- flask 2.0
- sqlite3 
- twilio 7.8.1 
	Twilio: A Python helper library that makes it easy to interact with the Twilio API.

- python-dateutil 2.8.2
	python-dateutil: This library provides powerful extensions to the standard datetime module already provided by Python.

- python-dotenv 0.20.0
	A library for importing environment variables from a .env file.

- APScheduler 3.9.1
	Advanced Python Scheduler (APScheduler) is a Python library that lets you schedule your Python code to be executed later, either just once or periodically. 
	https://pypi.org/project/APScheduler/

- Flask-APScheduler 1.12.3
	Flask-APScheduler is a Flask extension which adds support for the APScheduler.
	https://github.com/viniciuschiele/flask-apscheduler


## Initial Installation
Create  flaskr/.env file
*Add following TWILIO configuration in the .env file to send sms notification*

TWILIO_ACCOUNT_SID=xxxx
TWILIO_AUTH_TOKEN=xxxx
TWILIO_SMS_FROM=xxxx

*Add following EMAIL configuration in .env file to send email notifiaction*
EMAIL=youremail@example.com
EMAIL_PASSWORD=YOUR_MAIL_PASSWORD
SMTP_SERVER=YOUR_EMAIL_PROVIDER_SMTP_SERVER
SMTP_PORT=587

### Install dependacies requirements
- pip install requiremnts.txt

### Run following commands in shell
- export FLASK_APP=flaskr
- export FLASK_ENV=development
- flask init-db
- flask run

## To run other Instances
- export FLASK_APP=flaskr
- export FLASK_ENV=development
- flask run


