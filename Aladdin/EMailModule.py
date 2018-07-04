import smtplib
from email.mime.text import MIMEText
from email.header import Header
from Aladdin.LogModule import logging


sender = 'mingdeop@sina.com'
user = 'mingdeop@sina.com'
password = 'kemingjunde!@#'
smtp_server = 'smtp.sina.com'


def send_mail(title,recipients,content):
    try:
        message = MIMEText(content,'html','utf-8')
        message['From'] = Header(sender)
        message['To'] = Header('警告信息','utf-8')

        subject = title

        message['Subject'] = Header(subject,'utf-8')
        # try:
        server = smtplib.SMTP_SSL(smtp_server,465)
        server.login(user,password)
        server.sendmail(sender,recipients,message.as_string())
        return True
    except smtplib.SMTPException as e:
        logging.warning(title,'mail send fail',e)
        return False

