#!/usr/bin/env python2

import datetime
import time
import struct
import sys
import json
import Mqtt.SubPub as mqtt

storeSqlite = True


nodeName = {
  "2": "out",
  "3": "bedroom",
}

if storeSqlite:
    import sqlite3
    sqlite_file = '/home/pi/work/plot/db.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    


import time
def now():
    return time.strftime("%Y-%m-%d %H:%M:%S")


f = open("/var/www/html/temp/temp.txt", "a")
f.write("start\n")
f.flush()

from collections import namedtuple
dataset = namedtuple('dataset', 'nodeid, rssi, type, cnt, vcc, temp, humi, pres, txLev')

import SerialData
test = SerialData.SerialData()
test.open()

lastRx = {} #key is nodeid, value is time

while True:
    test.readData()
            
    #data = "".join([chr(letter) for letter in test.DATA])
    data = test.DATA
    pkttype, cnt, vcc, temp, humi, pres, txPowerLevel = struct.unpack('BBhhhhB', data)
    d = dataset(test.SENDERID, test.RSSI, pkttype, cnt, float(vcc)/1000, float(temp)/100, float(humi)/100, float(pres)/10, txPowerLevel)
    #print d.temp
    #d.temp /= 100
    #d.humi /= 100
    #d.vcc /= 100
    
    tNow = time.time()
    tLast = lastRx.get(d.nodeid, tNow)
    tStr = now()
    str = "%s, %d sec, (%d byte), %s" % (tStr, tNow - tLast, len(test.DATA), d)
    print(str)

    f.write(str+"\n")
    f.flush()
    lastRx[d.nodeid] = tNow
    #print d
    #print 
    #print dataset

    if mqtt:
        nid = d.nodeid
        name = nodeName.get(nid, nid)
        mqtt.publish("sensor/%s/msg" % name, json.dumps(d._asdict()))
        text = "%.1fC" % d.temp
        if d.humi != 0.0:
            text = text + " %.1f%%" % d.humi
        mqtt.publish("sensor/%s/text" % name, text)
    
    if storeSqlite:
        cmd = "INSERT INTO data (timestamp, vcc, temp, humi) VALUES ('%s', %f, %f, %f)" % (tStr, d.vcc, d.temp, d.humi)
        conn.execute(cmd)
        conn.commit()
    
