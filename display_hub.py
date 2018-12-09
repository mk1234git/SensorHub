#!/usr/bin/env python2

import datetime
import time
import struct
import sys
import json

import SerialData
test = SerialData.SerialData()
test.open()



import mosquitto
import time
      

#test.writeDisplay("00Hallo\x0001Test\x00")
test.displayBegin()
test.displayText(0, 0, "Zeile 1")
test.displayText(0, 1, "Zeile 2")
test.displayText(0, 2, "Zeile 3")
test.displayText(0, 3, "Zeile 4")
test.displayEnd()

#########################################################

def on_message(client, message):
    print "on_display_message", client, message.payload
    json_str = str(message.payload.decode("utf-8"))
    msg = json.loads(json_str)
    test.displayBegin()
    for m in msg:
        test.displayText(m["x"], m["y"], m["text"])
    test.displayEnd()
#########################################################

client = mosquitto.Mosquitto("display_hub")
client.connect("localhost", 1883, 60)

client.subscribe("display/text", qos=0)
client.on_message=on_message        #attach function to callback

while True:
    #print "work"
    client.loop()

