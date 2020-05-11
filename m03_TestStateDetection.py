# -*- coding: utf-8 -*-
'''
This script performs state detection based on the previous calibration.

Running the script will create a console output [TILT,ROT] of the 
    detected state. The output is displayed only if it is different
    from the current state and under certain conditions defined 
    below to get a smooth output signal.
'''

#%% IMPORT & FIG
import numpy as np
from numpy import array, amin
from m97_sensorCom import readSensor, getXMCserialConnection
from m99_BfieldSimulation import simulateField13V as simulateField
from m00_Config import CONFIG
import time


# provide location with device calibration data
folder = CONFIG['folder']
filename = CONFIG['filenameTols']

# load data
tols = np.load(folder+filename+'.npy')

# create look-up table by simulation
Bs = simulateField(tols,360)
Bs = Bs.reshape((5*360,3))


#%%
# #open serial connection
ser = getXMCserialConnection()

# start algorithm --------------------------------------------------
field_BUFFER = np.zeros((2,3))     #fields buffer
state_BUFFER = np.zeros(3)         #states buffer

# current state (different representations)
DSTATE = [999,999]      #dstate \in [0-5,0-71] = [tilt,rot]   [99,99] for undefined

# this function simply fixes the definition of the tilt 
#   numbers according to the documentation.
def outpFix(dstate):
    if dstate[0] == 999:
        return [999,dstate[1]]      
    if dstate[0] == 0:
        return ['Center',dstate[1]]
    if dstate[0] == 4:
        return ['Forward',dstate[1]]
    if dstate[0] == 1:
        return ['Left',dstate[1]]
    if dstate[0] == 3:
        return ['Back',dstate[1]]
    if dstate[0] == 2:
        return ['Right',dstate[1]]
    
    
    



DSTATE = [999,999]
   

while 1:

        B = readSensor(ser)
        dists = np.linalg.norm(Bs-B,axis=1)
        argMin = np.argmin(dists)
        Min = dists[argMin]
    
        # the following code is only there to provide a cleaned up an nice
        #   output by simple algorithmic means. This can surely be improved.
    
        
        # how close are we to the nearest state?
        if Min > 90:  # "undefined state" when one is in-between tilts
            newDSTATE = [999,999]
            if DSTATE != [999,999]:
                DSTATE = [999,999]
                #print(outpFix(DSTATE))
    
        else:
            newSTATE = argMin
            newDSTATE = [int(newSTATE/360),newSTATE%360]
    
            # conditions if the detected state should be set as new state
            condition1 = (newDSTATE[0] != DSTATE[0])           # different tilt
            condition2 = (abs(newDSTATE[1] - DSTATE[1]) > 0.9) # avoid neighboring rotations
    
            if condition1 or condition2:
                DSTATE = newDSTATE
                print(outpFix(DSTATE))
                
               
               
               
    
    
    
    


