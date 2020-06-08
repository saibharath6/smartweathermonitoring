import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
import json
#Provide your IBM Watson Device Credentials
organization = "zajnh3"
deviceType = "raspberrypi"
deviceId = "1234567"
authMethod = "token"
authToken = "12345678"

# Initialize GPIO

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='motoron':
                print("motor is on")
        elif i=='motoroff':
                print("motor is off")

try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)#.............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
    x=requests.get('http://api.openweathermap.org/data/2.5/weather?q=Hyderabad,%20IN&appid=7a5e89f1d05a183ab2436a71b8238030')
    a=json.loads(x.text)
    b=a["main"]
    temp=b["temp"]
    press=b["pressure"]
    hum=b["humidity"]
    soilm=random.randint(0,100)
    #Send Temperature & Humidity to IBM Watson
    data = { 'Temperature' : temp, 'Humidity': hum, 'Pressure': press, 'soilmoisture' : soilm }
    #print (data)
    def myOnPublishCallback():
        print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % hum, "Pressure = %s " % press, "Soilmoisture = %s %%" % soilm, "to IBM Watson")

    success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not connected to IoTF")
    time.sleep(2)
        
    deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()

