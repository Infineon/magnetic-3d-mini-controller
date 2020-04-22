# -*- coding: utf-8 -*-
'''
functions for communication with XMC

This script requires the package "pyserial" NOT the "serial" package,
despite being imported through serial.
Installation: e.g. 'pip install pyserial' in conda prompt

In many cases (e.g. Spyder) the serial port is not closed after program execution.
In such a case one can close the port using the "ser.close()" command.
'''

import numpy as np
import serial
import serial.tools.list_ports
import sys

def readSensor(serial):
    # communicate with XMC to read out the sensor
    # returns B-field in [LSB]

    try:
        # request data    
        serial.write('s\n'.encode('utf8'))
        # receiving and parsing
        msg_b = serial.readline()
        msg_s = str(msg_b).split(",")
        bx,by,bz = msg_s[0],msg_s[1],msg_s[2]
        bx = bx.replace("b'","")
        bx = bx.replace("\\x00","")
        bz = bz.replace("\\n'","")
        B = np.array([int(bx),int(by),int(bz)]) #convert to int(self, parameter_list):
        return B

    except Exception as e:
        print('sensor communication broke down')
        print(str(e))
        serial.close() # Only executes once the loop exits
        sys.exit()



def getXMCserialConnection(): 
    # returns serial port object
    # opens the serial port to communicate with the XMC
    
    ports = list(serial.tools.list_ports.comports())
    if (len(ports) != 0):
        for p in ports:
            if ((p.pid == 261) & (p.vid == 4966)): # pid and vid from xmc
                print("XMC found on port: " + p.device)
                ser = serial.Serial(p.device, 19200)
                print('Serial Connection Done')
                return ser
    
    print('ERROR(getSerialConnection) - Cannot Find a device.')
    sys.exit()