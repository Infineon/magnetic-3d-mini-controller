# -*- coding: utf-8 -*-
'''
The following functions simulate the magnetic field so that it can
    directly be compared to the experiment

simulateFieldX(inp,N) returns an array of shape 5xNx3 for 
            5 Tilts, 
            N points on each circle, 
            3 components of the field
        in units of LSB (=sensor output, 1LSB~100uT through Mfac 
        base value = O(10))

Input Vars: these are variables that descibe possible system tolerances
    displM - sideways magnet displacement
    dCoT - distance of magnet from center of tilt
    gap - airgap magnet-sensor
    Mfac - multiplicative factor to adjust magnet magnetization amplitude
    Sx,Sy - sensor xy position on PCB
    dy - magnet position
    TiltAngle TA1-TA4 - max tilt angle of the device in different directions
    A1,A2,A3 - rotation angles of sensor
    OffX,OffY,OffZ - sensor offset
    Mx,My,Mz - magnetization direction

Not all variables may be chosen for simulateFieldX
'''

#%% MAIN
import numpy as np
import magpylib as magpy

def simulateField13V(inp,N):
    #get the magnetic field for the MID system using a 4x4x4 cubical magnet using the new vectorized code
    # N data points per tilt

    tol_displM, tol_dCoT, tol_gap, tol_Mfac, tol_TA1, tol_TA2, tol_TA3, tol_TA4, Sx, Sy, dy, dMx, dMz = inp
    
    #fixed values = base geometry
    displM0 = 1.8
    dCoT0 = 7
    gap0 = 2
    Mfac0 = 14
    TiltAngle0 = 10
    a,b,c = 4,4,4

    #final values including tolerances
    displM = displM0 + tol_displM
    dCoT = dCoT0 + tol_dCoT
    gap = gap0 + tol_gap
    Mfac = Mfac0 + tol_Mfac
    TA1 = TiltAngle0 + tol_TA1
    TA2 = TiltAngle0 + tol_TA2
    TA3 = TiltAngle0 + tol_TA3
    TA4 = TiltAngle0 + tol_TA4
    Mx, My,Mz = dMx*Mfac, -1000*Mfac, dMz*Mfac

    mag = np.array([Mx,My,Mz])
    dim = np.array([a,b,c])
    posm = np.array([displM,dy,c/2+gap])
    poso = np.array([Sx,Sy,0])
    anch = np.array([0,0,gap+c+dCoT])

    #code vectorization
    MAG = np.tile(mag,(N*5,1))  
    DIM = np.tile(dim,(N*5,1))
    POSo = np.tile(poso,(N*5,1))
    POSm = np.tile(posm,(N*5,1))

    #MAG = np.array([mag]*(N*5))
    #DIM = np.array([dim]*(N*5))
    #POSo = np.array([posS]*(N*5))
    #POSm = np.array([posM]*(N*5))

    temp = np.linspace(0,360,N+1)[:-1]
    ANG1 = np.concatenate((temp,temp,temp,temp,temp))

    ax1 = np.array([0,0,1])
    AX1 = np.tile(ax1,(N*5,1))
    ANCH = np.tile(anch,(N*5,1))

    #ANCH = np.array([anch]*(5*N))
    ANG2 = np.concatenate((np.zeros(N),np.ones(N)*TA1,np.ones(N)*TA2,np.ones(N)*TA3,np.ones(N)*TA4))
    
    a1 = np.array([0,0,1])
    ta1 = np.tile(a1,(N,1))
    
    a2 = np.array([1,0,0])
    ta2 = np.tile(a2,(N,1))
    
    a3 = np.array([-1,0,0])
    ta3 = np.tile(a3,(N,1))

    a4 = np.array([0,1,0])
    ta4 = np.tile(a4,(N,1))
    
    a5 = np.array([0,-1,0])
    ta5 = np.tile(a5,(N,1))
    
    #AX2 = np.array([[0,0,1]]*N + [[1,0,0]]*N + [[-1,0,0]]*N + [[0,1,0]]*N + [[0,-1,0]]*N)
    AX2 = np.concatenate((ta1,ta2,ta3,ta4,ta5))

    Bv = magpy.vector.getBv_magnet('box',MAG,DIM,POSm,POSo,[ANG1,ANG2],[AX1,AX2],[ANCH,ANCH])

    return np.reshape(Bv,(5,N,3))


