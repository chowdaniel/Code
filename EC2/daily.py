#!/usr/bin/python

import datetime
from pytz import timezone
import csv
import Cross
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

emailfrom = "chowwwdaniel@gmail.com"
emailto = 'danielchow798@gmail.com'
fileToSend = '/home/ubuntu/cron/VOL.csv'
username = "AKIAIWSAL4JMDN63G4WA"
password = "Asdx0FUTwhN6PJPFkbgkVcFvNwKmF9m5doEz06dPw1kw"

curr = datetime.datetime.now()
out = 'SMA Crossover ' + curr.strftime('%-d/%m/%Y')

msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = out
msg.preamble = "message"

#For Error

FROM = "chowwwdaniel@gmail.com"
TO = ['danielchow798@gmail.com']
SUBJECT = out

def run():
    
    error = False
    TEXT = ''
    
    curr = datetime.datetime.now(timezone('Asia/Singapore'))
    temp = open('/home/ubuntu/cron/VOL.csv','w')
    a = csv.writer(temp)
    txt = 'Generated on ' + curr.strftime('%d/%m/%Y %-H:%M:%S')

    a.writerows([[txt]])
    a.writerows([['Ticker','Symbol','Volume','Price','First','Last','Max','SMA','%','Date','No.Days']])

    try:
        s = open('/home/ubuntu/cron/SYM.csv','r')
        sy = csv.reader(s)
        symbols = []

        for i in sy:
            symbols.append(i)
    except:
        error = True
        TEXT = TEXT + 'SYM File Error\n'

    end = datetime.datetime.now()
    start = datetime.datetime(end.year-1, 1, end.month)

    line = []
    res = []
    out = []

    for sym in symbols:
        try:
            out = Cross.run(sym[0],start,end)
            if len(out) == 0:
                continue
            
            line = sym
            line.append(out[1])
            line.append(out[2])
            res.append(line)
            line = []
        except:
            line = sym
            line.append('ERROR')
            line.append(999)
            res.append(line)
            line = []
            continue

    res.sort(key=lambda x:x[10])

    for i in res:
        a.writerows([i])
    
    temp.close()
    send(TEXT,error)
    
def send(text,error):
    if error == False:
        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

        server = smtplib.SMTP("email-smtp.us-west-2.amazonaws.com")
        server.starttls()
        server.login(username,password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        
    else:
        message = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (FROM, ", ".join(TO), SUBJECT, text)

        server = smtplib.SMTP("email-smtp.us-west-2.amazonaws.com")
        server.starttls()
        server.login(username,password)
        server.sendmail(FROM, TO, message)
        server.quit()

run()
