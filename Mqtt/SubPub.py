#!/usr/bin/python

import mosquitto
    
client = mosquitto.Mosquitto("")
client.connect("localhost", 1883, 60*60)

def publish(topic, payload, qos=0, retain=True):
    client.publish(topic, payload, qos, retain)

if __name__ == "__main__":
    publish("mytopic", payload=12, qos=0, retain=True)    

