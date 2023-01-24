# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from lib import *
import pub_thingsboard, sub_sensors
import multiprocessing

p1 = multiprocessing.Process(target=pub_thingsboard.run)
p2 = multiprocessing.Process(target=sub_sensors.run)
if __name__ == '__main__':
    p1.start()
    p2.start()
    #client = mqtt.Client()
  #  client.on_connect = on_connect
  #  client.on_message = on_message

    #client.connect(broker, 1883, 61)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    #client.loop_forever()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
