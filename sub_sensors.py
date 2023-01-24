from lib import on_message, on_connect, broker, mqtt


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883, 61)

client.loop_forever()