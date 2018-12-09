#!/usr/bin/env python2

import datetime
import time
import struct
import sys
import json
import Mqtt.SubPub as mqtt


if mqtt:
    pub = mqtt.Mqtt("sensor_hub")

storeSqlite = False
writeText = False

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

if writeText:
    f = open("/var/www/html/temp/temp.txt", "a")
    f.write("start\n")
    f.flush()
else:
    f = None
    
from collections import namedtuple
dataset = namedtuple('dataset', 'nodeid, rssi, type, cnt, vcc, temp, humi, pres, txLev')
ryncreq = namedtuple('dataset', 'nodeid, rssi, type, cnt, vcc')


import SerialData
test = SerialData.SerialData()
test.open()

if False:
    #test.writeDisplay("00Hallo\x0001Test\x00")
    test.displayBegin()
    test.displayText(0, 0, "Zeile 1")
    test.displayText(0, 1, "Zeile 2")
    test.displayText(0, 2, "Zeile 3")
    test.displayText(0, 3, "Zeile 4")
    test.displayEnd()


lastRx = {} #key is nodeid, value is time

while True:
    test.readData()
            
    #data = "".join([chr(letter) for letter in test.DATA])
    if test.DATALEN < 4:
        continue
    
    data = test.DATA
    pkttype, cnt, vcc = struct.unpack('BBh', data[0:4])
    vcc = float(vcc)/1000
    if pkttype == 1:
        temp, humi, pres, txPowerLevel = struct.unpack('hhhB', data[4:])
        d = dataset(test.SENDERID, test.RSSI, pkttype, cnt, vcc, float(temp)/100, float(humi)/100, float(pres)/10, txPowerLevel)
        #print d.temp
        #d.temp /= 100
        #d.humi /= 100
        #d.vcc /= 100
    else:
        print test.SENDERID, test.RSSI, pkttype, test.DATA
        d = ryncreq(test.SENDERID, test.RSSI, pkttype, cnt, vcc)
        
    tNow = time.time()
    tLast = lastRx.get(d.nodeid, tNow)
    tStr = now()
    str = "%s, %d sec, (%d byte), %s" % (tStr, tNow - tLast, len(test.DATA), d)
    print(str)

    if f:
        f.write(str+"\n")
        f.flush()
    lastRx[d.nodeid] = tNow
    #print d
    #print 
    #print dataset

    if pkttype == 1:
        if mqtt:
            nid = d.nodeid
            name = nodeName.get(nid, nid)
            pub.publish("sensor/%s/msg" % name, json.dumps(d._asdict()))
            text = "%.1fC" % d.temp
            if d.humi != 0.0:
                text = text + " %.1f%%" % d.humi
            topic = "sensor/%s/text" % name
            print "publish:", topic, text
            pub.publish(topic, text)
    
        if storeSqlite:
            cmd = "INSERT INTO data (timestamp, vcc, temp, humi) VALUES ('%s', %f, %f, %f)" % (tStr, d.vcc, d.temp, d.humi)
            conn.execute(cmd)
            conn.commit()
    
