import requests
import json
import threading
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

accidentDataFetched = None
accidentDataPostResponse = None

class PostAccidentSignalData:
    def __init__(self, rsuId, accidentLongitude, accidentLatitude, accidentVehicleId):
        self.rsuId = rsuId
        self.accidentLongitude = accidentLongitude
        self.accidentLatitude = accidentLatitude
        self.accidentVehicleId = accidentVehicleId

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
        if "statusCode" in message.message:
            print(message.message)
        else:
            jsonAccident = message.message
            print(jsonAccident)
            jsonAccident['rsuId']="RSU-3"
            postAccidentSignals(jsonAccident)
        
def fetchAccidentSignals(url):
    response = requests.get(url)
    accidentDataFetched = response.json()
    print("Data received from Cloud !")
    pubnub.publish().channel("RSU-3").message(accidentDataFetched).pn_async(my_publish_callback)
    time.sleep(2)
    threading.Timer(2.0, fetchAccidentSignals(fetchUrl)).start()

def postAccidentSignals(data):
    accidentSignalData = PostAccidentSignalData(data['rsuId'],data['accidentVehicleId'], data['accidentLatitude'], data['accidentLongitude'])
    jsonStr = json.dumps(accidentSignalData.__dict__)
    print("Data to be transferred to cloud - ")
    print(jsonStr)
    response = requests.post(postUrl, jsonStr)
    print(response)

fetchUrl = "https://hi6s5iimc1.execute-api.eu-west-1.amazonaws.com/DeployFinal"
postUrl = "https://ehbcunqxzi.execute-api.eu-west-1.amazonaws.com/DeployFinal"


def main():

    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels("RSU-3").execute()

    fetchAccidentSignals(fetchUrl)
    
    
if __name__ == "__main__":
    main()