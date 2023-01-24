import os
import time
import sys
import json
import random
import paho.mqtt.client as mqtt
import ssl
import statistics
from lib import temp_list, soil_list, timeToWater, get_flow, CONT_MAX, pub_lists, THINGSBOARD_HOST, ACCESS_TOKEN


client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.tls_set(certfile=None,
               keyfile=None,
               cert_reqs= ssl.CERT_REQUIRED)
client.connect(THINGSBOARD_HOST, 8883)
client.loop_start()
while(1):
    if temp_list == CONT_MAX:
        pub_lists()
        client.publish('v1/devices/me/telemetry', json.dumps(
        {'tank': "1", 'timeMin': str(timeToWater(temp=statistics.mean(temp_list), hum=statistics.mean(soil_list))),
         'flow': str(get_flow())}))

client.loop_stop()
client.disconnect()