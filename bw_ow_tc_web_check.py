#!-*- coding:utf8 -*-
#Author:Clay@lwork.com
#Description:用于监控所有的TW2版本每个服务器的TW web状态.
#Note:别随便删除
__author__ = 'Administrator'
import httplib2
import ConfigParser
import requests
import time
import json
import socket 


#全局变量
hostname = socket.gethostname()
PORT = 80

#定义上传监控数据对象
def updata(project,status):

	ts = int(time.time())
	payload = [
	    {
	        "endpoint": "%s"%hostname,
	        "metric": "HK.web.%s.check"%project,
	        "timestamp": ts,
	        "step": 60,
	        "value": int(status),
	        "counterType": "GAUGE",
	        "tags": "webcheck,project=all",
	    },
	
	]
	print payload
	
	r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload))
	
	print r.text

#获取服务器主机名，测试域名
cf = ConfigParser.ConfigParser()
cf.read("/cron/weburl.cfg")
it = cf.items("url")
for tuple in it:
	project = tuple[0]
	URL = tuple[1]
	#print URL
	try:
		h = httplib2.Http(timeout=10)
		response,content = h.request(URL)
		if response.status > 399:
        		status = 0
    		else:
        		status = 1
		#print response.status
	except Exception, e:
    		status = 0
	#print status
	updata(project,status)

