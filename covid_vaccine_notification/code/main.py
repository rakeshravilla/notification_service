import requests
import json
import smtplib
import traceback
from datetime import datetime, timedelta
import time
import sys
import pandas as pd
from tabulate import tabulate


def send():
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, send_to, email_text)
        server.close()
        print('Notified..')
    except:
        print('Something went wrong...')
        traceback.print_exc()


def fetch_sessions(n):
    
    dateval = datetime.strftime(datetime.now() + timedelta(n), '%d-%m-%y')
    
    cowin_url = r"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pin}&date={date}".format(pin=pinval, date=dateval)
    cowin_url1 = r"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={date}".format(pin=pinval, date=dateval)
    r = requests.get(cowin_url)
    r1 = requests.get(cowin_url1)
    
    cowin_return = json.dumps(json.loads(r.text)['sessions'], indent=2)
    cowin_return1 = json.dumps(json.loads(r1.text)['sessions'], indent=2)
    return cowin_return,cowin_return1
        

curr_time = datetime.strftime(datetime.now(), '%d-%m-%y %H:%M:%S')
global pinval
pinval = sys.argv[1] #enter pincode of area to scan

global gmail_user
gmail_user = <sender-gmail-id>
global gmail_password
gmail_password = <sender-gmail-password>
global sent_from
sent_from = gmail_user
global send_to
send_to = sys.argv[2].split(',') #enter comma separated gmail-id's to send mail to
global subject
subject = 'Urgent: Cowin Notification for pincode {}'.format(pinval)
global body

df_union=df_week_union=""

for i in range(10):
  try:
    df1,df1_week=fetch_sessions(i)
    
    df_union=df1+"\n"+df_union
    df_week_union=df1+"\n"+df_week_union
  except:
    pass

if df_union.strip()=="" and df_week_union.strip()=="":
    sys.exit('No Sessions Available, exiting..')
    pass
if df_union.strip()=="":
    df_union='No Sessions Available'
if df_week_union.strip()=="":
    df_week_union='No Sessions Available'

body = """Time: {}

Dear Recipient,

This message is a notification for vaccination for pincode {}. Book ASAP. Stay alert at all times.

Sessions Tomorrow:
{}



===============================


Sessions This Week:
{}
""".format(curr_time,pinval, df_union, df_week_union)

global email_text
email_text = """\
From: {}
To: {}
Subject: {}

{}
""".format(sent_from, ", ".join(send_to), subject, body)

print(curr_time)

print(body)

send()

print('Recipient(s) {} for pincode {}'.format(','.join(send_to),pinval))