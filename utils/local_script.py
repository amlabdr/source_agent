# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 11:25:54 2022

Controlling script for the CLD1015 compact laser driver; Each device is uniquely identified
with a serial number.

@author: yns19
"""

import socketserver
import socket
import yaml
import threading
import pyvisa
import time    

#PYVISA package is required for interfacing measurement devices
class CLD1015():
    
    def __init__(self, serialNumber='M00819452'):
        rm=pyvisa.ResourceManager()
        deviceList=rm.list_resources()
        
        #looking through the device list
        for i in deviceList:
            print(i)
            if serialNumber in i:
                device=i
                print("laser driver found, device ID:", device)
                FoundDevice=True
            else:
                print("Cannot find laser driver:", i)
                break
                
            if FoundDevice:
                try:
                    self.CLD1015=rm.open_resource(device)
                    print("CLD1015 connected.")
                except OSError:
                    print('Cannot open device')
                 
    #switching on laser
    def laser_on(self):
        self.CLD1015.write("OUTP 1")
        time.sleep(0.5)
        print('laser on.')
    
    #switching off laser    
    def laser_off(self):
        self.CLD1015.write("OUTP 0")
        time.sleep(0.5)
        print('laser off.')
    
    #switching on tec PID loop
    def tec_on(self):
        self.CLD1015.write("OUTP2 1")
        time.sleep(0.5)
        print('tec on.')
            
    #switching off tec PID loop
    def tec_off(self):
        self.CLD1015.write("OUTP2 0")
        time.sleep(0.5)
        print('tec off.')
    
    #setting laser current, input current in units of Amps; max current allowed is 0.12A
    def set_laser_current(self, current=0):
        if current > 0.12:
            print("exceeding the laser current limit!")
            self.CLD1015.write("SOUR:CURR:LEV:AMPL 0)")
        else:
            self.CLD1015.write("SOUR:CURR:LEV:AMPL "+str(current))
            time.sleep(0.5)
            print("laser current set to "+str(current))
    
    #request a status update in ascii
    def show_status(self):
        print("-------------------------------------------------------------------------")
        print(self.CLD1015.query("*IDN?"))
        print("{0: >30}".format("Laser on? 1(yes)/0(no):"), self.CLD1015.query("OUTP?"),end='')
        print("{0: >30}".format("TEC on? 1(yes)/0(no):"), self.CLD1015.query("OUTP2?"),end='')
        self.CLD1015.write("CONF:TEMP")
        temp=self.CLD1015.query("READ?")
        self.CLD1015.write("CONF:CURR")
        curr=self.CLD1015.query("READ?")
        self.CLD1015.write("CONF:VOLT")
        volt=self.CLD1015.query("READ?")
        print("{0: >30}".format('Laser temperature:'),"{0}".format(temp),end='')
        print("{0: >30}".format('Laser current:'),"{0}".format(curr),end='')
        print("{0: >30}".format("Forward voltage:"),"{0}".format(volt),end='')
    
    #disconnect the laser driver
    def disconnect(self):
        self.CLD1015.close()
        print('CLD1015 disconnected.')
    
if __name__ == '__main__':
    laserdriver = CLD1015()
    laserdriver.tec_off()
    laserdriver.laser_off()
    #laser current should be entered in units of Amps
    #laserdriver.set_laser_current(0.1)
    laserdriver.show_status()
    laserdriver.disconnect()
    