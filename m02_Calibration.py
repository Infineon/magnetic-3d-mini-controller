# -*- coding: utf-8 -*-
'''
This script performs the calibration process based on the
    provided dataset. It will determine the mechanical
    tolerances of the system and store them for later use
    when creating a look-up table.
    
First make sure that the experimental data created in m01
    is pointed at correctly and that 'filename' is set correctly
    as to how you want to store the result (see m00_Config).
    
    Then just run the script.

ADDITIONAL INFO: The script uses a genetic evolution algorithm
    to fit the data sample onto the analytical solution provided
    by the magpylib library. The fitting variables are a set of
    selected mechanical and magnetic tolerances. 
'''

#%% 5-circle calib
import numpy as np
import scipy.optimize as opt
from lib.m98_magMapEval import distToCircV
from m00_Config import CONFIG

# load experimental data
folder = CONFIG['folder']
filename = CONFIG['filenameCalib']
datE = np.load(folder+filename+'.npy')
datE = np.array([datE[0],datE[2],datE[4],datE[3],datE[1]]) #align components

# for storage of result
filename = CONFIG['filenameTols']

# define the cost function  
def costBad2(tols): #mean squared badness
    distToGoodCircV,distToBadCircV = distToCircV(datE,tols,200)
    BAD2 = np.sum((distToGoodCircV/distToBadCircV)**2)/20 #20 values in datE
    return BAD2


# optimization procedure --------------------------------------------------
if __name__ == "__main__": #mupltiprocessing guard

    print('---------------------------')         #text output
    print('Starting calibration scheme')         #text output

    #define boundaries of tolerances
    bound_displM = (-1,1)       # magnet displacement [mm]
    bound_dCoT = (-1,1)         # distance to CoT [mm]
    bound_gap = (-.5,.5)        # airgap [mm]
    bound_Mfac = (-3,3)         # magnetization factor []
    bound_TA = (-3,3)           # tilt angles [deg]
    bound_S = (-1,1)            # sensor displacements from center [mm]
    bound_dy = (-1,1)           # magnet displacement2 [mm]
    bound_M = (-150,150)        # additional off-axis magnetizations[mT]
    
    #collect boundaries for DE algorithm
    bounds = [bound_displM,bound_dCoT, bound_gap,bound_Mfac,
              bound_TA,bound_TA,bound_TA,bound_TA,
              bound_S,bound_S,bound_dy,
              bound_M,bound_M]
    
    # choose good popsize, maxiter, workers to achieve 
    #     good precision (< 0.01) in acceptable time
    # Further time-improvements can be made by reducing the number of fitting variables
    result = opt.differential_evolution(costBad2,
                                        bounds,
                                        popsize=10,
                                        maxiter=250,
                                        disp=True,
                                        polish=False,
                                        workers=4,
                                        tol=0.01,
                                        updating='deferred')

    # store result
    np.save(folder + filename,result.x)

    print(result.message)                        #text output
    print('Storing tolerances in ' +  filename + '.npy')    #text output
    if result.fun > 0.02:
        print('#########################')
        print('Optimization score: {}'.format(result.fun))
        print('Please start the calibration process again (m01_StoreCalibData.py) and follow the instructions carefully. The optimization score is higher than the acceptable value (0.02)')

