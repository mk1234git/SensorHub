#!/usr/bin/python


import paho.mqtt.client as mqtt #import the client1
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    print("Subscribing to topic")
    client.subscribe("sensor/#")

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

client = mqtt.Client("abc", protocol=mqtt.MQTTv31) #create new instance
client.on_message=on_message
client.on_connect=on_connect

print("connecting to broker")
client.connect("127.0.0.1", 1883, 60*60) #connect to broker
#client.connect("iot.eclipse.org", 1883, 60)

#client.loop_forever()
client.loop_start()
while True:
    time.sleep(1)
