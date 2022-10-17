'''
Created on Oct 17 11:25:54 2022

Controlling agent  for the CLD1015 compact laser driver; Each device is uniquely identified
with a serial number.

@author: amlabdr
'''
#standards imports
import json, logging, time, yaml
from threading import Thread

#imports to use AMQP 1.0 communication protocol
from protocols.send import Send
from protocols.receive import RecvSpecification
from proton.reactor import Container

def send_capability(url,topic,period,capabilityData):
    while True:
        # Publish Capability in "/capabilities"
        Container(Send(url,topic, capabilityData)).run()
        print('capability sent')
        time.sleep(period)



#read configuration file
yf    = open('config/config.yaml','r')
config = yaml.load(yf, Loader=yaml.SafeLoader)
yf.close()

PERIOD = config["controller"]["capability_period"]
url = config["controller"]["IP"] + config["controller"]["port"]

#publishing the agent capability
capabilityFile = open('config/capability.json', 'r')
capabilityData = json.load(capabilityFile)
capabilityFile.close()
topic = 'topic://'+'/capabilities'
thread_send_capability = Thread(target=send_capability, args=(url,topic,PERIOD,capabilityData))
thread_send_capability.start()

#start lesstning for a specification from the controller
topic='topic://'+capabilityData['endpoint']+'/specifications'
Container(RecvSpecification(url,topic)).run()