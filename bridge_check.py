# -*- coding: utf-8 -*-
'''
user:clay.bbs@gmail.com
date:2015-12-1
desc:used to check bridge status
'''

import socket
import time
import requests
import json
import ConfigParser


def bridgecheck(ip,port):
    request_str = '''{"id":200001,
                            "payload_class":"HeartbeatMessage",
                            "payload_data":{},
                            "service":"system",
                            "version":"1.0.0"}'''

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        sock.send(request_str)
        data = sock.recv(4096)
        sock.close()
        temp = eval(data)['payload_data']
        if int(temp['error_code']) == 0:
            status = 1
	    return status
    except socket.error,b:
            status = 0
	    return status

def updata(status):
    hostname = socket.gethostname()
    ts = int(time.time())
    payload = [
		{
			"endpoint": "%s" % hostname,
			"metric": "bw3.newbridge.check",
			"timestamp": ts,
			"step": 60,
			"value": int(status),
			"counterType": "GAUGE",
			"tags": "bridgecheck,project=bw3",
		},

	]
    print payload

    r = requests.post("http://203.88.167.42:1988/v1/push", data=json.dumps(payload))

    print r.text



if __name__ == '__main__':
        socket.setdefaulttimeout(10)
        cf = ConfigParser.ConfigParser()
        cf.read("bridge_ip_port.cfg")
        temp = cf.items("ports")
        for tuple in temp:
            PORT = tuple[1]
            status = bridgecheck('23.91.98.128',int(PORT))
	    updata(status)
