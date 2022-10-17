'''
Created on Oct 17 11:25:54 2022

Controlling agent  for the CLD1015 compact laser driver; Each device is uniquely identified
with a serial number.

@author: amlabdr
'''
#standards imports
import json, logging
from threading import Thread

#imports to use AMQP 1.0 communication protocol
from protocols.send import Send
from proton.reactor import Container

