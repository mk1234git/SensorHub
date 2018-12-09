#!/usr/bin/python

import Mqtt.SubPub as mqtt
import json
import time
import datetime

text=[]

pub = mqtt.Mqtt("display")

def dispText(x,y,str):
    text.append({"x":x, "y":y, "text": str})

def clearText():
    del text[:]

msgStore = {}    
    
def update_display():
    clearText()
    y = 0
    time_str = time.strftime("%H:%M:%S %d.%m.")
    dispText(0, y, time_str)
    y += 1
    
    out = msgStore.get(4, None)
    if out: #out
        temp = out["temp"]
        pres = out["pres"]
        t_str = "%4.1fC %dhPa" % (temp, pres)
        dispText(0, y, t_str)
        y += 1

    out2 = msgStore.get(2, None)
    if out2: 
        temp = out2["temp"]
        humi = out2["humi"]
        t_str = "%4.1fC %4.1f%%" % (temp, humi)
        dispText(0, y, t_str)
        y += 1

    schlafen = msgStore.get(3, None)
    if schlafen:
        temp = schlafen["temp"]
        humi = schlafen["humi"]
        t_str = "%4.1fC %4.1f%%" % (temp, humi)
        dispText(0, y, t_str)
        y += 1

    json_str = json.dumps(text)
    print json_str
    pub.publish("display/text", json_str)

    
def on_message(client, message):
    json_str = str(message.payload.decode("utf-8"))
    msg = json.loads(json_str)
    print msg
    nodeid = msg["nodeid"]
    print nodeid
    msgStore[nodeid] = msg
    update_display()

                                    
                                
if __name__ == "__main__":
    import mosquitto
    import time
                                            
    client = mosquitto.Mosquitto("display_client")
    client.connect("localhost", 1883, 60)
                                                    
    #client.subscribe("sensor/4/msg", qos=0)
    #client.subscribe("sensor/3/msg", qos=0)
    client.subscribe("sensor/+/msg", qos=0)
    client.on_message=on_message        #attach function to callback
                                     
    last_minute = -1
    while True:
        client.loop()
        now = datetime.datetime.now()
        if now.minute != last_minute:
            last_minute = now.minute
            update_display()
            
        
            