#!/usr/bin/python

import sys
import json

from urllib import urlencode
import urllib2

import wu
import math

myheight = 300

WU_URL = "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"

def hpa_to_inches(pressure_in_hpa):
    pressure_in_inches_of_m = pressure_in_hpa * 0.02953
    return pressure_in_inches_of_m

#pressure correction to sea level 
#https://de.wikipedia.org/wiki/Barometrische_Hoehenformel
#https://rechneronline.de/barometer/
def pres_corr(pres_hpa, temp_c, height):
    T_C = temp_c + 273.15
    return pres_hpa * math.pow(T_C / (T_C + 0.0065*height), -5.255)

    
# From http://wiki.wunderground.com/index.php/PWS_-_Upload_Protocol
def wu_upload(temp_c, pres_hpa=None, humi=None):
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
    if pres_hpa != None:
        baromin = hpa_to_inches(pres_corr(pres_hpa, temp_c, myheight))
        weather_data["baromin"] = str(baromin)
        #print pres_hpa
        #print temp_c
        #print myheight
        #print pres_corr(pres_hpa, temp_c, myheight)
        
    if humi != None:
        weather_data["humidity"] = "%.2f" % humi
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


def on_message(client, message):
    json_str = str(message.payload.decode("utf-8"))
    msg = json.loads(json_str)
    temp_c = msg["temp"]
    pres_hpa = msg["pres"]
    humi = msg["humi"]
    print ""
    print time.strftime("%H:%M:%S")
    wu_upload(temp_c, pres_hpa, humi)
    
        
if __name__ == "__main__":
    import mosquitto
    import time
        
    client = mosquitto.Mosquitto("wu_upload")
    client.connect("localhost", 1883, 60)
        
    client.subscribe("sensor/2/msg", qos=0)
    client.on_message=on_message        #attach function to callback
    
    if True:
        while True:
            client.loop()
    else:
        client.loop_start()
        
        while True:
            time.sleep(1)