#!-*- coding:utf8 -*-
# Author:Clay@lwork.com
# Description:用于监控实施返佣中每个客户的返佣状态
# Note:别随便删除

import httplib
import ConfigParser
import requests
import time
import json
import socket
import os


# 全局变量
hostname = socket.gethostname()
os.chdir('/cron')


# 定义上传监控数据对象
def updata(webnode, status):
	ts = int(time.time())
	payload = [
		{
			"endpoint": "%s" % hostname,
			"metric": "bw.wbnode.%s" % webnode,
			"timestamp": ts,
			"step": 60,
			"value": int(status),
			"counterType": "GAUGE",
			"tags": "webnode.check,project=BW",
		},

	]
	print payload

	r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload))

	print r.text


# 获取服务器主机名，测试域名
cf = ConfigParser.ConfigParser()
cfgfile = os.getcwd() + '/' + 'node.cfg'
cf.read(cfgfile)
it = cf.items("node")
for tuple in it:
	URL = tuple[0]
	nodename = tuple[1]
	if nodename[:2] == 'ow':
		PORT = 8081
	else:
		PORT = 8080
	try:
		http = httplib.HTTPConnection(URL, PORT, timeout=5)
		http.request('GET', '/')
		response = http.getresponse()
		status = 1
		#print response.reason
    		#if response.status > 399:
        	#	status = 0
    		#else:
        	#	status = 1
		#response = http.getresponse()
		#print response.status
		#print response.reason
	except Exception, e:
		status = 0
	#print status
	updata(nodename, status)
