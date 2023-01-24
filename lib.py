import operator
from datetime import datetime
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import random
import json
import ssl
import statistics

# Global variables
THINGSBOARD_HOST = 'srv-iot.diatel.upm.es'
ACCESS_TOKEN = '3qLLqP02I6b3z4laOxYB'
ACCESS_TOKEN2 = 'IpH1DYoT4aM0n3vKTtRE'
time_list = []
temp_list = []
soil_list = []
cont = 0
TEMP_MAX = 100
CONT_MAX = 10  # 3600
TEMP_LIMIT = 28
HUM_LIMIT = 60
broker = "broker.mqtt-dashboard.com"
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'



def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("tree/sensor/#")

def check_list(temp, soil):
    # send data from lists to Thingsboard
    client = mqtt.Client()
    client.username_pw_set(ACCESS_TOKEN)
    client.tls_set(certfile=None,
                   keyfile=None,
                   cert_reqs=ssl.CERT_REQUIRED)
    client.connect(THINGSBOARD_HOST, 8883)
    client.loop_start()
    if len(temp) == CONT_MAX:
        if timeToWater(temp=statistics.mean(temp), hum=statistics.mean(soil)) > 0:
            client.publish('v1/devices/me/telemetry', json.dumps({'tank': "1",'timeMin': str(timeToWater(temp=statistics.mean(temp), hum=statistics.mean(soil))), 'flow': str(get_flow())}))
    else:
        client.publish('v1/devices/me/telemetry', json.dumps({'tank': "0"}))
    client.loop_stop()
    client.disconnect()


def on_message(client, userdata, msg):
    print(msg.topic)
    check_list(temp_list, soil_list)
    if msg.topic == 'tree/sensor/temp':
        time_list.append(round(datetime.timestamp(datetime.now())))
        temp_fl = float(msg.payload.decode('utf8'))
        temp_list.append(temp_fl)

    if msg.topic == 'tree/sensor/soil':
        time_list.append(round(datetime.timestamp(datetime.now())))
        soil_fl = float(msg.payload.decode('utf8'))
        soil_list.append(soil_fl)
    print(time_list)


def pub_lists(time, temp, soil):
    # send data from lists to Thingsboard
    client = mqtt.Client()
    client.username_pw_set(ACCESS_TOKEN2)
    client.tls_set(certfile=None,
                   keyfile=None,
                   cert_reqs=ssl.CERT_REQUIRED)
    client.connect(THINGSBOARD_HOST, 8883)
    for i in range(0, len(time)):
        client.publish('v1/devices/me/telemetry', json.dumps({'ts': time[i], 'temp': temp[i], 'hum': soil[i], 'light': 0}))


def remove_list():
    time_list.remove()
    temp_list.remove()
    soil_list.remove()


def toWater(temp=TEMP_LIMIT-1, hum=HUM_LIMIT+1):
    order = False
    if temp > TEMP_LIMIT or hum < HUM_LIMIT:
        order = True
    return order


def timeToWater(temp=TEMP_LIMIT-1, hum=HUM_LIMIT+1):
    timeMin = 0
    if toWater(temp, hum):
        if temp < 30 or hum > 58:
            timeMin = 5
        if temp < 32 or hum > 56:
            timeMin = 10
        if temp < 34 or hum > 55:
            timeMin = 15
        if temp < 36 or hum > 54:
            timeMin = 20
        if temp >= 36 or hum > 53:
            timeMin = 25
    return timeMin


def get_flow():
    # get the current day of the year
    doy = datetime.today().timetuple().tm_yday

    # "day of year" ranges for the northern hemisphere
    spring = range(80, 172)
    summer = range(172, 264)
    fall = range(264, 355)
    # winter = everything else
    if doy in spring:
        flow = 75
    elif doy in summer:
        flow = 100
    elif doy in fall:
        flow = 50
    else:
        flow = 25

    return flow