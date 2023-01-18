import paho.mqtt.client as mqtt

datos_l = list()
datos = {'Temp': 0 , 'Hum': 0, 'Light': 0 }
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("plane/control/pressure/external")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("message")
    #print(msg.topic+" "+str(msg.payload)+'\n')
    dat_s=str(msg.payload).split("'")
    print(msg.payload)
    datos_l.append(int(dat_s[1]))
    print(datos_l)
    datos['Light'] = datos_l
    #print(datos_l)
    print("Datos")
    print(datos)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()