import paho.mqtt.client as mqtt
import os
import configparser
import pymongo
from pymongo import MongoClient
import json

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    mqttc.subscribe(zonetopic, 0)

def on_message(client, obj, msg):
    createOrSaveZoneUpdate(msg.payload)

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def createOrSaveZoneUpdate(locationUpdate):
    data = json.loads(locationUpdate)
    deviceLocation = location.find_one({'device_id': data['device_id']})
    if deviceLocation == None :
        print('Simply Insert')
        location.insert_one(data)
    else:
        print('Update Record')
        location.update_one(
            {"device_id": deviceLocation['device_id']},
            {
                "$set": {
                     "zone":data['zone']
                }
            }
        )
        print(deviceLocation)


mqttc = mqtt.Client()
config = configparser.ConfigParser()
config.read('config.ini')
mqtt = config['MQTT']
mongo = config['MONGO']

hostname = mqtt['host']
port = int(mqtt['port'])
username = mqtt['username']
password = mqtt['password']
zonetopic = mqtt['zonetopic']

mongo_host = mongo['host']
mongo_port = int(mongo['port'])

# Mongo Client
client = MongoClient(mongo_host, mongo_port)
mining_db = client['mining']
location = mining_db.device

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Connect
mqttc.username_pw_set(username, password)
mqttc.connect(hostname, port)

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = mqttc.loop()

print("rc: " + str(rc))