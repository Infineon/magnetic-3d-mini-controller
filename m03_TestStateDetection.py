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
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bokeh.client import push_session

# provide location with device calibration data
folder = CONFIG['folder']
filename = CONFIG['filenameTols']

# load data
tols = np.load(folder+filename+'.npy')

# create look-up table by simulation
Bs = simulateField(tols,72)
Bs = Bs.reshape((5*72,3))


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
        return [0,dstate[1]]
    if dstate[0] == 4:
        return [1,dstate[1]]
    if dstate[0] == 1:
        return [2,dstate[1]]
    if dstate[0] == 3:
        return [3,dstate[1]]
    if dstate[0] == 2:
        return [4,dstate[1]]
    
    
    
def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y






def update():
    field_BUFFER = np.zeros((2,3)) 
    DSTATE = [999,999]
   

    while 1:
    
        # store state in buffer - working with a buffer takes  moving average
        #       this slows down the readout, but avoids flickering to some extend
        B = readSensor(ser)
        field_BUFFER = np.roll(field_BUFFER,1,axis=0)
        field_BUFFER[0] = B
        field_BUF_av = np.mean(field_BUFFER,axis=0)
    
        # compare to look-up, determine closest
        dists = np.linalg.norm(Bs-field_BUF_av,axis=1)
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
            newDSTATE = [int(newSTATE/72),newSTATE%72]
    
            # conditions if the detected state should be set as new state
            condition1 = (newDSTATE[0] != DSTATE[0])           # different tilt
            condition2 = (abs(newDSTATE[1] - DSTATE[1]) > 0.7) # avoid neighboring rotations
    
            if condition1 or condition2:
                DSTATE = newDSTATE
                print(outpFix(DSTATE))
                phi = np.radians(90+5*DSTATE[1])
                x,y = pol2cart(5,phi)
               
               
                source.stream(dict(X = [0,x],Y=[0,y]),2)
    
    
    
    
source = ColumnDataSource(dict(X = [0,1], Y = [0,1]))
p = figure(plot_height=400, plot_width=400, title="Radar Plotter",x_range=[-5,5],y_range=[-5,5])


p.line(x ="X", y="Y",line_width = 2, source=source, color = 'red')
doc = curdoc()
doc.add_root(p)
doc.add_periodic_callback(update, 1000)

