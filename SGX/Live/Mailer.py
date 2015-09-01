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
fileToSend = 'VOL.csv'
username = "AKIAIWSAL4JMDN63G4WA"
password = "Asdx0FUTwhN6PJPFkbgkVcFvNwKmF9m5doEz06dPw1kw"

msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = "Subject test"
msg.preamble = "message"

def send():
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

send()    