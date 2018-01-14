#!/usr/bin/python

import time
import serial
import binascii

testData = [
  "id: 3, rssi: -84, len: 8, data: 0100C60A8007B914\n"
  
]

class SerialData:
    defaultDev = "/dev/serial/by-id/usb-SparkFun_SparkFun_Pro_Micro-if00"
    def __init__(self):
        self.testIdx = 0
    
    def open(self, dev=defaultDev):
        self.serial = serial.Serial(dev)
        
    def readData(self):
        data = self.serial.readline()
        print data
        self.decode(data)

    def readTestData(self):
        self.decode(testData[self.testIdx])
        self.testIdx += 1
                
    def testDecode(self):
        for data in testData:
            self.decode(data)
            print "SENDERID: ", self.SENDERID, "RSSI: ", self.RSSI, "DATALEN: ", self.DATALEN, "DATA: ", binascii.hexlify(self.DATA)
            print(type(self.DATA), len(self.DATA))
        
    def decode(self, data):
        tags = data.split(',')
        for e in tags:
            #print e
            k,v = e.split(':')
            k = k.strip()
            v = v.strip()
            
            if k == 'id':
                self.SENDERID = int(v)
            elif k == 'rssi':
                self.RSSI = int(v)
            elif k == 'len':
                self.DATALEN = int(v)
            elif k == 'data':
                self.DATA = binascii.unhexlify(v)

        
if __name__ == "__main__":
    t = SerialData()
    
    print t.testDecode()
    
    while True:
        print t.readData()
        