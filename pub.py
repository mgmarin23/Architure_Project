import random
import time

from paho.mqtt import client as mqtt_client
broker = 'localhost'
port = 1883
# generate client ID with pub prefix randomly
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



def pub_mobile(client, topic,msg):
    print(msg)
    client.publish(topic, msg, qos=1)


if __name__ == '__main__':
    # first message from control tower
    client = connect_mqtt()

    while(1):
        msg = input('Configure time: ')
        pub_mobile(client, "tree/conf/time","25")
        msg = input('Configure Tª: ')
        pub_mobile(client, "tree/conf/temp","25")
        msg = input('Configure Soil %: ')
        pub_mobile(client, "tree/conf/soil","25")
        time.sleep(3)

    client.disconnect()