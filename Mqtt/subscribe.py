#!/usr/bin/python

import mosquitto
import time
    
client = mosquitto.Mosquitto()
client.connect("localhost", 1883, 60)


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    
client.subscribe("mytopic", qos=0)
client.on_message=on_message        #attach function to callback

client.loop_start()
while True:
    time.sleep(1)