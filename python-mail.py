# -*- coding: utf-8 -*-
"""
author:Clay
Date:2015-12-09
Description:Used to check mt4 report server status
"""

import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email.mime.text import MIMEText

def send_mail(From,to,messages):
    #COMMASPACE = ','
    msg = MIMEMultipart()
    msg['From'] = From
    msg['To'] = to
    msg['Subject'] = 'tx smtp check'
    msg['Date'] = formatdate(localtime=True)
# 构造MIMEText对象做为邮件显示内容并附加到根容器
    txt = MIMEText(messages)
    msg.attach(txt)
#发送邮件
    smtp = smtplib.SMTP_SSL()
    try:
        smtp.connect('smtp.exmail.qq.com:465')
        smtp.login('tss@lwork.com', 'abc123')
        smtp.sendmail(From, to, msg.as_string())
        smtp.quit()
    except Exception,e:
        print e

if __name__ == '__main__':
        From = 'tss@lwork.com'
        to = 'clay@lwork.com'
        send_mail(From,to,'tencent send SSL mail test')
