import paho.mqtt.client as mqtt
import os
import configparser
import pymongo
from pymongo import MongoClient
import json

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    mqttc.subscribe(stopetopic, 0)

def on_message(client, obj, msg):
    saveOrUpdateStopeData(msg.payload)

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def saveOrUpdateStopeData(locationUpdate):
    #Update Stope Data
    data = json.loads(locationUpdate)
    stopeData = stope.find_one({'stope_name': data['stope_name']})
    num_of_mobile_assets=0
    if stopeData == None :
        print('Simply Insert')
        mobile_asset_data = data['mobile_assets']
        if mobile_asset_data != None:
            if len(mobile_asset_data) > 0 :
                for mobile_asset in mobile_asset_data:
                    num_of_mobile_assets += mobile_asset['mobile_asset_number']
        data['mobile_assets'] = num_of_mobile_assets
        print(mobile_asset_data)
        stope.insert_one(data)
    else:
        print('Update Record')
        mobile_asset_data = data['mobile_assets']
        if mobile_asset_data != None:
            if len(mobile_asset_data) > 0 :
                for mobile_asset in mobile_asset_data:
                    num_of_mobile_assets += mobile_asset['mobile_asset_number']
        data['mobile_assets'] = num_of_mobile_assets
        stope.update_one(
            {"stope_name": data['stope_name']},
            {
                "$set": {
                    "number_of_people":data['number_of_people'],
                    "ready_to_geofence":data['ready_to_geofence'],
                    "is_geofenced":data['is_geofenced'],
                    "zone_id":data['zone_id'],
                    "ventilator_speed":data['ventilator_speed'],
                    "fall_alert":data['fall_alert'],
                    "SO2":data['SO2'],
                    "O2":data['O2'],
                    "CO":data['CO'],
                    "mobile_assets":num_of_mobile_assets
                    }
            }
        )

    #Update Stope Mobile Asset
    if mobile_asset_data != None:
        if len(mobile_asset_data) > 0 :
            deleteQuery = { "stope_name": data['stope_name'] }
            stope_moving_asset.delete_many(deleteQuery)
            for moving_asset in mobile_asset_data:
                moving_asset['stope_name']=data['stope_name']
                stope_moving_asset.insert_one(moving_asset)


mqttc = mqtt.Client()
config = configparser.ConfigParser()
config.read('config.ini')
mqtt = config['MQTT']
mongo = config['MONGO']

hostname = mqtt['host']
port = int(mqtt['port'])
username = mqtt['username']
password = mqtt['password']
stopetopic = mqtt['stopetopic']

mongo_host = mongo['host']
mongo_port = int(mongo['port'])

# Mongo Client
client = MongoClient(mongo_host, mongo_port)
mining_db = client['mining']
stope = mining_db.stope
stope_moving_asset = mining_db.stope_moving_asset

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