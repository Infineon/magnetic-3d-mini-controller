import numpy as np
import tkinter as tk
import threading
from tkinter import messagebox as tkMessageBox
from lib.m96_visualization import IDriveVisualizer
from lib.m97_sensorCom import readSensor, getXMCserialConnection
from lib.m99_BfieldSimulation import simulateField13V as simulateField
from m00_Config import CONFIG


# load calibration data
folder = CONFIG['folder']
filename = CONFIG['filenameTols']
tols = np.load(folder+filename+'.npy')


class IDriveCommunicator(threading.Thread):

    def __init__(self,iDriveVisualizer):
        threading.Thread.__init__(self)
        
        self.iDriveVisualizer = iDriveVisualizer
        
        self.ser = getXMCserialConnection()

        self.Bs = (simulateField(tols,72)).reshape((5*72,3))

   
    def run(self):

        # start algorithm --------------------------------------------------
        field_BUFFER = np.zeros((2,3))     #fields buffer

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
                return [2,dstate[1]]
            if dstate[0] == 1:
                return [3,dstate[1]]
            if dstate[0] == 3:
                return [1,dstate[1]]
            if dstate[0] == 2:
                return [4,dstate[1]]


        while True:
            
            B = readSensor(self.ser)

            #field_BUFFER = np.roll(field_BUFFER,1,axis=0)
            #field_BUFFER[0] = B
            #field_BUF_av = np.mean(field_BUFFER,axis=0)

            # compare to look-up, determine closest
            dists = np.linalg.norm(self.Bs-B,axis=1)
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
                condition2 = (abs(newDSTATE[1] - DSTATE[1]) > .1) # avoid neighboring rotations

                if condition1 or condition2:
                    DSTATE = newDSTATE

                    self.iDriveVisualizer.setState([outpFix(DSTATE)[0],DSTATE[1]])

                    print(outpFix(DSTATE))


#initialize classes
root = tk.Tk('iDrive Visualizer')
iDriveVisualizer = IDriveVisualizer(root)

iDriveCom = IDriveCommunicator(iDriveVisualizer)
iDriveCom.start()



#closing the tk window
def on_closing():
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        iDriveCom.CONNECTED = False
        iDriveCom.ser.close()
        exit()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
