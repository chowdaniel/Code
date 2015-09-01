#!/usr/bin/python

import smtplib
import datetime
from pytz import timezone
import pandas.io.data as web

XELp = 33.14
CMSp = 32.239
XELu = -200
CMSu = 200

past = (XELp * XELu) + (CMSp * CMSu)

curr = datetime.datetime.now(timezone('Asia/Singapore'))

end = datetime.datetime.now()
start = datetime.datetime(end.year-1, end.month, end.day)

first = web.DataReader('XEL', "yahoo", start, end)
second = web.DataReader('CMS', "yahoo", start, end)

XELn = first['Adj Close'][-1]
CMSn = second['Adj Close'][-1]

curr = (XELn * XELu) + (CMSn * CMSu)

change = curr - past

TEXT = 'XEL: ' + str(XELp) + '/' + str(XELn) + ' - ' + str(XELn-XELp) + '\n'
TEXT = TEXT + 'CMS: ' + str(CMSp) + '/' + str(CMSn) + ' - ' + str(CMSn-CMSp) + '\n\n'
TEXT = TEXT + 'Profit: ' + str(change)

FROM = "chowwwdaniel@gmail.com"
TO = ['danielchow798@gmail.com']
username = "AKIAIWSAL4JMDN63G4WA"
password = "Asdx0FUTwhN6PJPFkbgkVcFvNwKmF9m5doEz06dPw1kw"

SUBJECT = 'XEL CMS MR'

message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

server = smtplib.SMTP("email-smtp.us-west-2.amazonaws.com")
server.starttls()
server.login(username,password)
server.sendmail(FROM, TO, message)
server.quit()
