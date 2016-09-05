# -*- coding: utf-8 -*-
#!/usr/bin/python


__author__ = 'Clay Chen'

import sys
from flask import Flask, jsonify
from flask import make_response
from flask import request
import smtplib
import string
import threading
import unicodedata
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email.mime.text import MIMEText
from email.header import Header

#reload(sys)
#sys.setdefaultencoding("utf-8")

app = Flask(__name__)
# app.config.update(
#     DEBUG=True,
#     SERVER_NAME='192.168.0.108:7000'
# )


@app.route('/sendmail/api/v1.0/mail', methods=['POST'])
def send_mail():

    mail_user = 'alert'
    mail_postfix = 'lwork.com'
    COMMASPACE = ','
    list_temp = request.form['tos']
    List = string.splitfields(list_temp.encode("utf-8"),",")
    conten_temp = request.form['content']
    #编码转换，request.form获取的编码格式为unicode,先转换成utf-8,在转换成unicode编码，编码邮件客户端中文乱码。
    content = conten_temp.encode("utf-8")
    subject = request.form['subject'].encode("utf-8")
    status = []
    try:
        From = u'Falcon monitor'+"<"+mail_user+"@"+mail_postfix+">"
        msg = MIMEMultipart()
        msg['From'] = From
        #msg['To'] = ','.join(To)
        msg['To'] = ','.join(List)
       # msg['To'] = to
        msg['Subject'] = Header(subject,'utf-8')
        msg['Date'] = formatdate(localtime = True )


        txt = MIMEText(content,'plain','utf-8')
        msg.attach(txt)

	    smtp = smtplib.SMTP_SSL()
        smtp2 = smtplib.SMTP
        smtp.connect('smtp.exmail.qq.com:465')
        smtp.login('alert@lwork.com', 'leanwork123')
        smtp.sendmail(From,List,msg.as_string())
        smtp.quit()
        status.append('ok')
    except Exception,e:
        status.append(e)
    ###############################################
    task = {
        'status': status[0]
    }
    return jsonify({'response': task}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': '500'}), 500)


if __name__ == '__main__':
    #app.run(debug=True,host='10.252.74.15',port=8099)
    app.run(debug=True,host='10.252.74.15',port=8099,threaded=True)
    app.run(processes=10)
