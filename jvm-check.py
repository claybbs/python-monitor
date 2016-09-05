#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author:Clay
Date:'15-11-20'
Description:Used to get jvm 
"""
from __future__ import division
from pyjolokia import Jolokia
import time
import socket
import requests
import json

j4p = Jolokia('http://10.8.15.28:8778/jolokia/')

#------------------add request----------------------------
j4p.add_request(type = 'read', mbean='java.lang:type=Threading',attribute='ThreadCount')
j4p.add_request(type = 'read', mbean='java.lang:type=Memory')

hulb = j4p.getRequests()
threadcount = hulb[0]['value']
memhulb = hulb[1]['value']

#------------------------
#堆最大值
heapmem = memhulb['HeapMemoryUsage']
#堆当前分配值
Heapcommit = heapmem['committed']
#堆当前使用值
Heapused = heapmem['used']
#堆使用率
HeapMemoryUsagepercent = "%.3f%%" % (float(Heapused)/float(Heapcommit)*100)

#--------------------------
Nonpmem = memhulb['NonHeapMemoryUsage']
#非堆当前分配值
NonHeapcommit = Nonpmem['committed']
#非堆当前使用值
NonHeapused = Nonpmem['used']
#非堆使用率
NonHeapMemoryUsagepercent = "%.3f%%" % (float(NonHeapused)/float(NonHeapcommit)*100)

hostname = socket.gethostname()
ts = int(time.time())
payload = [
    {
        "endpoint": "%s"%hostname,
        "metric": "Heap.Memory.Usagepercent",
        "timestamp": ts,
        "step": 60,
        "value": HeapMemoryUsagepercent,
        "counterType": "GAUGE",
        "tags": "tomcat jmx",
    },
#]
#payload1 = [
    {
        "endpoint": "%s"%hostname,
        "metric": "NonHeap.Memory.Usagepercent",
        "timestamp": ts,
        "step": 60,
        "value": NonHeapMemoryUsagepercent,
        "counterType": "GAUGE",
        "tags": "tomcat jmx",
    },
#]
#payload2 = [
    {
        "endpoint": "%s"%hostname,
        "metric": "Threadcount",
        "timestamp": ts,
        "step": 60,
        "value": threadcount,
        "counterType": "GAUGE",
        "tags": "tomcat jmx",
    },

]

r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload))
#r1 = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload1))
#r2 = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload2))
print r.text
