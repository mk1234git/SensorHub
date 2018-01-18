#!/usr/bin/python

import sys
import json

from urllib import urlencode
import urllib2

import wu

WU_URL = "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"

# From http://wiki.wunderground.com/index.php/PWS_-_Upload_Protocol
def wu_upload(temp_c):
    print("Uploading data to Weather Underground")
    # build a weather data object
    weather_data = {
    "action": "updateraw",
    "ID": wu.station_id,
    "PASSWORD": wu.station_key,
    "dateutc": "now",
    }
    if temp_c != None:
        temp_f = temp_c * 1.8 + 32 
        weather_data["tempf"] = str(temp_f)
    #"humidity": str(humidity),
    #"baromin": str(pressure),

    upload_url = WU_URL + "?" + urlencode(weather_data)
    print(upload_url)
    response = urllib2.urlopen(upload_url)
    html = response.read()
    print("Server response:", html)
    # do something
    response.close()  # best practice to close the file

    #try:
    #except:
    #    print("Exception:", sys.exc_info()[0])


def on_message(client, userdata, message):
    json_str = str(message.payload.decode("utf-8"))
    msg = json.loads(json_str)
    temp_c = msg["temp"]
    wu_upload(temp_c)
    
        
if __name__ == "__main__":
    import mosquitto
    import time
        
    client = mosquitto.Mosquitto()
    client.connect("localhost", 1883, 60)
        
    client.subscribe("sensor/2/msg", qos=0)
    client.on_message=on_message        #attach function to callback
                        
    client.loop_start()
        
    while True:
        time.sleep(1)