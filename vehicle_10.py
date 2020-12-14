from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import sched,time
import os
import threading
from geopy.distance import geodesic
import socket
from datetime import datetime, timedelta
import json

pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-cbac1ba8-84b2-469d-a59b-7d66d9b4cb2a'
pnconfig.subscribe_key = 'sub-c-88b6488e-3adb-11eb-b6eb-96faa39b9528'
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

accidentDataPostResponse = None

def storeAccidentData(message):
    accidentDataFetched = []
    if "body" in message:
        print("Accident message received \n",message)
        output = message['body']
        print(output)
        for acccidentSignal in output:
            timestamp = acccidentSignal['timeStamp']
            date_time_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            if abs(datetime.now() - date_time_obj) < timedelta(minutes=500):
                accidentDataFetched.append(acccidentSignal)
            print("******")
        return accidentDataFetched
    else:
        return accidentDataFetched

def my_publish_callback(envelope, status):
   # Check whether request successfully completed or not
    if not status.is_error():
        pass
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        if message.message == None:
            continue_moving()
        else:
            print("From RSU-5 : ",message.message, "\n")
            time.sleep(0.5)
            continue_moving(message.message)

#RSU 5
RSU_coords = [53.377350, -6.248184]
vehicle_10_start_coords = [53.378550, -6.247462]
junction_coords = [53.375804, -6.250268]

def continue_moving(message):
    accidentDataFetched = storeAccidentData(message)
    print(accidentDataFetched)
    pubnub.unsubscribe().channels("RSU-5").execute()
    if(len(accidentDataFetched) > 0):
        getToAccidentLocation(accidentDataFetched)
    else:
        print("No accidents detected ! \n")

def getToAccidentLocation(accidentDataFetched):
    pubnub.unsubscribe().channels("RSU-5").execute()
    accidentCount = len(accidentDataFetched)
    print(accidentCount, "accidents detected ! \n")
    vehicle_lane_change_coords = []
    arrayCounter = 0
    accident_coords = []
    for accidentLoc in accidentDataFetched:
        vehicle_lane_change_coords.append([accidentLoc['accidentLongitude'], accidentLoc['accidentLatitude']])
        accident_coords0= float(accidentLoc['accidentLongitude'])
        accident_coords1= float(accidentLoc['accidentLatitude'])
        accident_coords.append([accident_coords0,accident_coords1])
    print("Ambulance location", vehicle_10_start_coords, "\n")
    print("Accidents at", accident_coords, "\n")
    print("Junction location ", junction_coords, "\n")
    time.sleep(0.5)
    
    while((geodesic(vehicle_10_start_coords,junction_coords).m) > 15):
        print("Distance to Junction (metres): ",geodesic(vehicle_10_start_coords,junction_coords).m)
        vehicle_10_start_coords[0] = round((vehicle_10_start_coords[0] - 0.0003092),6)
        vehicle_10_start_coords[1] = round((vehicle_10_start_coords[1] - 0.0004172),6)
        print("Current Coordinates", vehicle_10_start_coords[0],vehicle_10_start_coords[1])
    print("\n Ambulance at junction.. \n")
    print("Taking a turn to reach accident location.. \n")
    time.sleep(0.7)
    print("Distance to Accident location (metres):", geodesic(junction_coords,accident_coords[0]).m, "\n")

    while(vehicle_10_start_coords[0] <= accident_coords0 and vehicle_10_start_coords[1] <= accident_coords1):
        vehicle_10_start_coords[0] = round((vehicle_10_start_coords[0] - 0.0029380),6)
        vehicle_10_start_coords[1] = round((vehicle_10_start_coords[1] + 0.0021096),6)
        print("Current Coordinates", vehicle_10_start_coords[0],vehicle_10_start_coords[1])
    print("Ambulance reached the accident location ! \n")

def moving_vehicle():
    while((geodesic(vehicle_10_start_coords,RSU_coords).m) > 15):
        print("Distance to RSU-5 (metres): ",geodesic(vehicle_10_start_coords,RSU_coords).m)
        time.sleep(0.5)
        vehicle_10_start_coords[0] = round((vehicle_10_start_coords[0] - 0.0002400),6)
        vehicle_10_start_coords[1] = round((vehicle_10_start_coords[1] - 0.0001444),6)
        print("Current Coordinates", vehicle_10_start_coords[0],vehicle_10_start_coords[1], "\n")
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels("RSU-5").execute()
moving_vehicle()