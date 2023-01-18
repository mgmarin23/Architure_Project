import os
import time
import sys
import json
import random
import paho.mqtt.client as mqtt
import ssl

THINGSBOARD_HOST = 'srv-iot.diatel.upm.es'
ACCESS_TOKEN = '3qLLqP02I6b3z4laOxYB'
# Function to read sensor values
'''def read_from_sensor():
    temp = random.randint(25,45)
    hum = random.randint(50,60)
    air = random.randint(55,60)
    light = random.randint(100,180)
    return temp, hum, air,light'''
# Thingsboard platform credentials


'''INTERVAL = 5
sensor_data = {'temperature' :0,'humidity':0,'air_quality':0,'light_intensity':0}
next_reading = time.time()'''
sensor_data = {'Status' : 1, 'Tree':24, 'Field':3, 'Water ml': 73}

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.tls_set(certfile=None,
               keyfile=None,
               cert_reqs=ssl.CERT_REQUIRED)
client.connect(THINGSBOARD_HOST,8883)
client.loop_start()

try:
    while True:
        #temp,hum,air,light = read_from_sensor()

        '''print("Temperature:",temp, chr(176) + "C")
        print("Humidity:", hum,"%rH")
        print("Air Quality:", air,"%")
        print("Light Intensity:",   light,"lux")
        
        sensor_data['temperature'] = temp
        sensor_data['humidity'] = hum
        sensor_data['air_quality'] = air
        sensor_data['light_intensity'] = light'''

        client.publish('v1/devices/me/telemetry',json.dumps(sensor_data))
        time.sleep(10)


except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()