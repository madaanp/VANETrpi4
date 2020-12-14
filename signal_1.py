from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import sched,time
import os
import threading
import socket
from twisted.internet import task, reactor

pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-cbac1ba8-84b2-469d-a59b-7d66d9b4cb2a'
pnconfig.subscribe_key = 'sub-c-88b6488e-3adb-11eb-b6eb-96faa39b9528'
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

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
        print("Signal: ",message.message)

signal_lat = 53.345856 
signal_long = -6.259210

signal_values = ["GREEN","ORANGE","RED"]

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("signal-1").execute()

signal_time = 5.0 #5 seconds
#Runs every 5 seconds
def operate_signal():
	pubnub.publish().channel("signal-1").message(str(signal_values[0])).pn_async(my_publish_callback)
	time.sleep(5)
	pubnub.publish().channel("signal-1").message(str(signal_values[1])).pn_async(my_publish_callback)
	time.sleep(5)
	pubnub.publish().channel("signal-1").message(str(signal_values[2])).pn_async(my_publish_callback)
	time.sleep(5)

l = task.LoopingCall(operate_signal)
l.start(signal_time)

reactor.run()
