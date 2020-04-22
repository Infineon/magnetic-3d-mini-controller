# -*- coding: utf-8 -*-
'''
This interactive script will store the user calibration data
The user is required to move the joystick to different,
designated positions. There are four rotation positions
rot1,rot2,rot3,rot4 that are indicated on the system knob and
five tilt positions:
    tilt0 = center
    tilt1 = towards uC
    tilt2 = to the right (uC pointing to you)
    tilt3 = away from uC
    tilt4 = to the left (uC pointing to you)

Before starting the script make sure that 'folder' and 'filename'
    are set correctly (m00_Config). This is where the calibration
    data will be stored for fitting in the next step.

Follow the steps below to create the caliration data:
    1. Rotate to start position = rot1 (and set tilt0)
    2. Start script (this will store [rot1,tilt0])
    3. Tilt to all four positions (first 1, then 2, then 3, then 4)
        Hold each position until screen output tells you to
        continue to the next one.
    4. When all five states are stored go to tilt0 and rotate to
        rot2 as demanded by the screen output.
    5. Continue like this until all 20 states are stored, at which
        point the script will automatically exit.

Comment: It was shown that 4-points per circle are enough to get the
calibration to work decently - hence this 4-rot position scheme
'''

#%% MAIN
import numpy as np
import time
from m97_sensorCom import readSensor, getXMCserialConnection
import winsound
from m00_Config import CONFIG

# calib data is stored here
folder = CONFIG['folder']
filename = CONFIG['filenameCalib']

# open sensor communication
ser = getXMCserialConnection()

# start read-out algorithm -----------------------------------------------
BUFFER = np.zeros((10,3))           #create a B-field buffer
CALIB_DATA = np.ones((20,3))*9999   #store found states (4 rotations * 5 tilts) here, allocate with large values

print('------------------------')                    # text output
print('Start calibration scheme')                    # text output 
S1 = [[i+1,j] for i in range(4) for j in range(5)]   # text output
S2 = (['Tilt']*4 + ['Rotate'])*4                     # text output

for ii,s1,s2 in zip(range(20),S1,S2):

    while 1:

        #store state in buffer
        B = readSensor(ser)
        BUFFER = np.roll(BUFFER,1,axis=0)
        BUFFER[0] = B

        BUF_av = np.mean(BUFFER,axis=0)                             # average Buffer-state
        dev_mean = np.mean(np.linalg.norm(BUFFER-BUF_av,axis=1))    # deviation from average in Buffer
        
        # if all Buffer-states are very similar we are in a stable position that will be stored
        if dev_mean < 2: # threshhold=2 seems good

            # test if this state was already stored
            minDist = np.amin(np.linalg.norm(CALIB_DATA-BUF_av,axis=1))   # min dist to other stored states
            if minDist > 160: 
                # different calib states are at least ~200LSB apart. By choosing a large threshhold
                #     here we avoid to accidently sample states that are close to each other. 
                #     E.g. after tilting we move back to the center. The system then detects a new stable
                #     center state that will be close to the first one. But because we have rotated the 
                #     system a little bit by accident it will not be very close. This must be caught by
                #     this theshhold.
                #     This is also the reason why we initialize CALIB_DATA with very 'distant' states.

                print('State ' + str(s1) + ' detected! '+s2+' to next position.')
                winsound.Beep(500,100)    # sound output when a new state is found.
                CALIB_DATA[ii] = BUF_av   # store new state
                break
        
        time.sleep(0.03) #control sensor-readout speed


# reshape CALIB_DATA and store
dat = CALIB_DATA.reshape((4,5,3))
dat = np.swapaxes(dat,0,1)
np.save(folder+filename,dat)
print('Calibration finished sucessfully')
print('storing calibration data in ' + folder + filename+'npy')