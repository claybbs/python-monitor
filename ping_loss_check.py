#!-*- coding:utf8 -*-
#Author:Clay@lwork.com
#Description:用于监控所有的TW2版本每个服务器的TW web状态.
#Note:别随便删除
__author__ = 'Administrator'
import ConfigParser
import requests
import time
import json
import ping
import socket


#全局变量
hostname = socket.gethostname()

#定义上传监控数据对象
def updata(HOSTNAME,status):

	ts = int(time.time())
	payload = [
	    {
	        "endpoint": "%s"%hostname,
	        "metric": "icmp.%s.check"%HOSTNAME,
	        "timestamp": ts,
	        "step": 60,
	        "value": int(status),
	        "counterType": "GAUGE",
	        "tags": "project=icmp",
	    },

	]
	print payload

#	r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload))

#	print r.text

#获取服务器主机名，测试域名
cf = ConfigParser.ConfigParser()
cf.read("ip.cfg")
it = cf.items("list")
for tuple in it:
    HOSTNAME = tuple[0]
    IP = tuple[1]
    #print URL
    try:
        result = ping.quiet_ping(IP,timeout=2,count=10,psize=64)
        if int(result[0]) == 100:
                status = 0
        elif int(result[0]) >= 20:
                status = 0
        elif int(result[2]) >= 90:
                status = 0
        else:
                status = 1
    except Exception, e:
        status = 0
#    print status
    updata(HOSTNAME,status)

