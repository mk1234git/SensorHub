#!/usr/bin/python

debug=True
paho=True

if paho:
    import paho.mqtt.client as mqtt    
else:
    import mosquitto

class Mqtt():
    def __init__(self, clientid="", msg_cb=None):
        if paho:
            self.client = mqtt.Client(clientid, protocol=mqtt.MQTTv31)
            self.client.on_message=msg_cb
        else:
            self.client = mosquitto.Mosquitto(clientid)
        self.client.connect("localhost", 1883, 60*60)
        

    def publish(self, topic, payload, qos=0, retain=True):
        self.client.publish(topic, payload, qos, retain)

    def subscribe(self, topic):
        self.client.subscribe(topic, qos=0)
        if debug:
            print "subscribe: ", topic

    def loop_start(self):
        self.client.loop_start()
        
    def loop(self):
        self.client.loop()
    
if __name__ == "__main__":
    import time

    def msg_cb(client, userdata, message):
        print str(message.payload)
        
    m = Mqtt("test", msg_cb)
    #m.publish("mytopic", payload=12, qos=0, retain=True)

    m.subscribe("sensor/#")
    m.subscribe("sensor/+/msg")
    m.subscribe("display/text")
    
    if paho:
        print "loop_start"
        m.loop_start()
        
        while True:
            time.sleep(1)
    else:
        while True:
            m.loop()
            time.sleep(1)
        

