#!-*- coding:utf8 -*-
#__author__ = 'Administrator'
import socket
import time
import yaml
import requests
import json

IP = '47.90.52.78'
PORT = 10801
URL = 'http://47.90.52.78:10800'

hostname = socket.gethostname()
PORT = 80

#定义上传监控数据对象
def updata(servername,status):
	ts = int(time.time())
	payload = [
	    {
	        "endpoint": "%s"%hostname,
	        "metric": "fd.micservice.%s.check"%servername,
	        "timestamp": ts,
	        "step": 60,
	        "value": int(status),
	        "counterType": "GAUGE",
	        "tags": "portcheck,project=feedwork",
	    },
	
	]
	print payload
	r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload))
	print r.text

#测试端口
def CHECK_PORT(list_file):
	f = open(list_file)
	y = yaml.load(f)
	f.close()
	service_items = y["services"]
	for item in service_items:
		service_name = item['name']
		service_ip = item['ip']
		service_port = item['port']
		print service_name,service_ip,type(service_port)
    	sok = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    	sok.settimeout(5)
    	try:
        	sok.connect((service_ip,service_port))
        	status = 1
    	except  Exception,e:
        	status = 0
		# updata(service_name,status)

if __name__ == '__main__':
	service_list = 'micro-services.cfg'
	CHECK_PORT(service_list)