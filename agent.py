'''
Created on Oct 17 11:25:54 2022

Controlling agent  for the CLD1015 compact laser driver; Each device is uniquely identified
with a serial number.

@author: amlabdr
'''
#standards imports
from asyncio.log import logger
import json, time, yaml
import logging
import traceback
from threading import Thread

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#imports to use AMQP 1.0 communication protocol
from utils.send import Send
from utils.receive import RecvSpecification
from proton.reactor import Container

def send_capability(url,topic,period,capabilityData):
    while True:
        # Publish Capability in "/capabilities"
        try:
            Container(Send(url,topic, capabilityData)).run()
            logging.info('capability sent')
        except Exception:
            logging.error("Agent can't send capability to the controller. Traceback:")
            traceback.print_exc()
        time.sleep(period)


if __name__ == '__main__':
    #read configuration file
    yf    = open('config/config.yaml','r')
    config = yaml.load(yf, Loader=yaml.SafeLoader)
    yf.close()

    PERIOD = config["controller"]["capability_period"]
    url = config["controller"]["IP"] +':'+ config["controller"]["port"]
    serialNumber = config["source"]["serial"]

    topic = 'topic://'+'/capabilities'
    #publishing the agent measurement capability
    capabilityFile = open('config/measurement_capability.json', 'r')
    measure_capabilityData = json.load(capabilityFile)
    capabilityFile.close()
    thread_send_capability = Thread(target=send_capability, args=(url,topic,PERIOD,measure_capabilityData))
    thread_send_capability.start()

    #publishing the agent command capability
    capabilityFile = open('config/command_capability.json', 'r')
    command_capabilityData = json.load(capabilityFile)
    capabilityFile.close()
    thread_send_capability = Thread(target=send_capability, args=(url,topic,PERIOD,command_capabilityData))
    thread_send_capability.start()


    #start lesstning for a specification from the controller
    topic='topic://'+command_capabilityData['endpoint']+'/specifications'
    logging.info("Agent will start lesstning for a specification from the controller")
    Container(RecvSpecification(url,topic,serialNumber)).run()