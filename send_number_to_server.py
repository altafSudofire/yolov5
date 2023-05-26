import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time
import json
import pdb
import datetime
from conf import MQTT_USER, MQTT_PASS

#mqttBroker ="mqtt.eclipseprojects.io" 

#client = mqtt.Client("Temperature_Inside")
#client.connect(mqttBroker)


# ls=[]
# def on_message(client, userdata, message):
#     counter=1
#     payload = json.loads(message.payload)
#     print("elog user 6: ",datetime.datetime.now() ,str(message.payload.decode("utf-8")),payload,counter)
#     ls.append(counter)
#     print(len(ls))


def send(MQTT_USER, MQTT_PASS, record):
    MQTT_HOST = "43.204.54.187"
    client = mqtt.Client()

    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.connect(MQTT_HOST, 1883, 60)
    # record={'ePark_id':'30839845F00C'}
    # {"device": "stream",
    # "number": num}
    client.loop_start()
    # client.subscribe('AllowUser' + record['number'],1)
    # client.on_message = on_message
    client.publish('VehicleNumberDetection', json.dumps(record),1)
    print(f"{record} is successfully published to client")
    # while True:
    # randNumber = randrange(20)
    # pdb.set_trace()
        # client.loop_start()
        
        # data=json.dumps(record)
        # client.publish("EParkDeviceActive", data)

        # print("Just published " + str(data) + " to topic TEMPERATURE")
        # client.subscribe('DeviceConfig' + record['imei_no'])
        
    time.sleep(1)