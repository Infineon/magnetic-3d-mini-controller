# -*- coding: utf-8 -*-
'''
Collection of mixed functions for evaluation of the magnetic map.
'''

#%% MAIN
import numpy as np
from lib.m99_BfieldSimulation import simulateField13V as simulateField

def distToCircV(datExp,tols,Nsimu):
    '''
    simulates the field from (tols,Nsimu)
    then determines the distances to the circles for each given experimental point
        1. the good distance = distance to the designated circle
        2. the bad distance = nearest non-designated circle
    
       tols   = tolerances for simulation using getBmin_vector
       datExp = experimental data of shape [5,Nexp,3]
       Nsimu  = circle approximation in simulation
    '''
    Nexp = len(datExp[0])

    Bs = simulateField(tols, Nsimu)
    dE = np.array([[datExp]*Nsimu]*5)
    dE = dE.swapaxes(1,3)
    dE = dE.swapaxes(0,2)
    mini = np.amin(np.linalg.norm(dE-Bs,axis=4),axis=3)

    #distance of each experimental state to its designated circle
    distToGoodCircV = np.diagonal(mini,axis1=0,axis2=2)

    #distance of each experimental state to the closest bad circle
    msk = np.array([np.diag([1]*5)]*Nexp).swapaxes(0,1)
    mini_msk = np.ma.masked_array(mini,mask = msk)
    distToBadCircV = np.amin(mini_msk,axis = 2)
    distToBadCircV = distToBadCircV.filled()

    return distToGoodCircV.swapaxes(0,1),distToBadCircV


def getBAD(dexp,tol):
    '''
    evaluate how well a system is calibrated.
        this returns the 10 worst badness values.
        badness value = distToGoodCirc / distToBadCirc
      dexp = sample of shape [5,N,3]
      tol for field simulation
    '''

    distToGoodCircV,distToBadCircV = distToCircV(dexp,tol,72) #Nsimu=72 from real lookUp table
    bad = distToGoodCircV/distToBadCircV
    bad_sort = np.sort(bad,axis = 1)
    idx = np.argsort(bad,axis = 1)

    print(distToGoodCircV.shape)
    print(distToBadCircV.shape)

    #print(bad_sort[:,-3:])
    #print(idx[:,-3:])
    #print('--')
    for i in range(5):
        print(distToGoodCircV[i,list(idx[i,-3:])])
        print(distToBadCircV[i,list(idx[i,-3:])])
    print('__')
    
    return bad_sort[:,-3:]

# test getBAD
'''
folder = 'data/device40/'    
datE = np.array([np.load(folder+'dataTILT%s.npy' %str(i)) for i in [0,3,4,1,2]])
TO = np.array([ 1.87767903e-01,  9.90578058e-01,  4.90618154e-01,  1.07845888e+00,
       -1.68159691e+00, -2.15671411e+00, -1.63360754e+00, -1.99686723e+00,
        2.51330524e-01,  4.27927415e-02,  3.04425693e-01,  1.20597989e+02,
        1.43016952e+01])
print(getBAD(datE,TO,360))
'''

# how to define a cost function based on badness using distToCircV
'''
folder = 'data/device40/'    
datE = np.array([np.load(folder+'dataTILT%s.npy' %str(i)) for i in [0,3,4,1,2]])
def costBad2V(tols): #mean squared badness
    distToGoodCircV,distToBadCircV = distToCircV(datE,tols,72)
    BAD2 = np.sum((distToGoodCircV/distToBadCircV)**2)/500 #500 values in datE
    return BAD2
'''


# how to calculate circle distances using distToCircV:
'''
datE = simulateField(np.zeros(13),360)
dc =distToCircV(datE,np.zeros(13),360)
print(np.amin(dc[1],axis=1))
'''


#determine the minimal on-circle state separation (of state 1, the others will 
    # be similar from symmetry
def onCircSep(Vars,N):
    Bs = simulateField(Vars,N)
    SEP = 9999
    for B1 in Bs[1]:
        for B2 in Bs[1]:
            if (B1 != B2).any():
                sep = np.linalg.norm(B1-B2)
                if sep < SEP:
                    SEP = sep
    return SEP

