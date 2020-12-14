from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import sched,time
import os
import threading
from geopy.distance import geodesic
import socket

pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-cbac1ba8-84b2-469d-a59b-7d66d9b4cb2a'
pnconfig.subscribe_key = 'sub-c-88b6488e-3adb-11eb-b6eb-96faa39b9528'
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

vehicle_9_start_coords = [53.345339,-6.258867]
vehicle_9_stop_coords = (53.350482,-6.260630)

def moving_vehicle():
    while((geodesic(vehicle_9_start_coords,vehicle_9_stop_coords).m) > 80):
        print("Distance to destination (metres): ",geodesic(vehicle_9_start_coords,vehicle_9_stop_coords).m)
        time.sleep(0.5)
        vehicle_9_start_coords[0] = round((vehicle_9_start_coords[0] + 0.0001),6)
        vehicle_9_start_coords[1] = round((vehicle_9_start_coords[1] + 0.0001),6)
        print("Current Coordinates", vehicle_9_start_coords[0],vehicle_9_start_coords[1])
    print("Vehicle reached desitination !")
moving_vehicle()