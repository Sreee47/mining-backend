Mining Backend Components
=========================

## To Send Zone Update
Topic      -> zoneupdate  
JSON Model -> 	{ "device_id" : "sdfsdf", "zone" : "zone2" }  


## Fall Detection
If fall is detected  
-> Send evac crew a message, plan and details  
-> Send evac plan to the person's wearable  

## To Trigger Alert in wearable from Unity  
Topic            -> evacupdate  
Payload Message  -> Any Message  

## To Send Stope Details (From Unity Via MQTT)  
Topic                     -> stopeupdate  
Message Payload Structure ->  
{  
  "stope_name" : "stope1",  
  "number_of_people": 2,  
  "temperature": 39.8,  
  "humidity": 40,  
  "is_geofenced": true,  
  "ready_to_geofence":false,
  "zone_id":"zone1",
  "fall_alert": false,
  "SO2": 20,
  "O2":70,
  "CO":10,
  "mobile_assets" : [  
    {  
      "mobile_asset_name" : "truck",  
      "mobile_asset_number" : 2  
    },  
    {  
      "mobile_asset_name" : "truck",  
      "mobile_asset_number" : 2  
    }  
    ]  
}  

## To Get All Stope Data (GET API) (For Web)  
URL    -> http://139.162.46.222:3000/api/stopes  
Output -> Array Of Stope Data  
[  
  {  
    "stope_name": "stope1",  
    "number_of_people": 2,  
    "temperature": 39.8,  
    "humidity": 40,  
    "mobile_assets": 5,  
    "is_geofenced": false,  
    "id": "5c0043146ed6b737e4893182"  
  }  
]  

## To Get Specific Stope Data (GET API)  (For Web)  
URL (Encoded)  -> http://139.162.46.222:3000/api/stopes?filter=%7B%22where%22%3A%7B%22stope_name%22%3A%22stope1%22%7D%7D   
(replace stope1 in last with desired stope name)  
Output -> Array Of Stope Data  
[  
  {  
    "stope_name": "stope1",  
    "number_of_people": 2,  
    "temperature": 39.8,  
    "humidity": 40,  
    "mobile_assets": 5,  
    "is_geofenced": false,  
    "id": "5c0043146ed6b737e4893182"  
  }  
]  
If no matches found empty array is returned  


## To Get Moving Asset For A Given Stope (GET API)  (For Web)  
URL (Encoded)  -> http://139.162.46.222:3000/api/stope_moving_assets?filter=%7B%22where%22%3A%7B%22stope_name%22%3A%22stope1%22%7D%7D
(replace stope1 in last with desired stope name)  
Output -> Array Of Moving Asset Data  
[  
  {  
    "stope_name": "stope1",  
    "mobile_asset_name": "truck",  
    "mobile_asset_number": 2,  
    "id": "5c0075163b77500e8b71d32f"  
  },  
  {  
    "stope_name": "stope1",  
    "mobile_asset_name": "tractor",  
    "mobile_asset_number": 2,  
    "id": "5c0075163b77500e8b71d330"  
  },  
  {  
    "stope_name": "stope1",  
    "mobile_asset_name": "dumper",  
    "mobile_asset_number": 1,  
    "id": "5c0075163b77500e8b71d331"  
  }  
]  
  
If no matches found empty array is returned  
  
You can browse the swagger @ http://139.162.46.222:3000/explorer




