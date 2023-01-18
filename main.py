# This is a sample Python script.
import json
import requests
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import Subscriber_MQTT

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #Lista
    datos_l = list()
    datos_t = list()
    datos_h = list()
    datos_s = list()

    for i in range(3):
        datos_l.append(i)
        datos_t.append(i)
        datos_h.append(i)
        datos_s.append(i)

    datos = {'Temp': 0 , 'Hum': 0, 'Light': 0 }

    datos['Temp'] = datos_t
    datos['Hum'] = datos_h
    datos['Light'] = datos_l
    datos['Soil'] = datos_s

    print(datos)

    # Pass diccionary to json write
    with open('Test.json', 'w') as outfile:
        json.dump(datos, outfile, indent=4)
    #Pass diccionary to json write
    '''for i in range(2):
    a = str(i) + '.json'
    print(a)
    with open(a,'w') as outfile:
        json.dump(datos,outfile,indent=4)
    '''
    #Read json
    with open("Test.json") as file:
        data = json.load(file)

    r = requests.post('https://srv-iot.diatel.upm.es/api/v1/IpH1DYoT4aM0n3vKTtRE/telemetry',None,data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
Subscriber_MQTT.on_message