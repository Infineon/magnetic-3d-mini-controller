
Mini i-Drive – Calibration & Test 

Code summary: The Mini-iDrive (MiD) code contains the following files:
1.	m00_Config.py
2.	m01_SoreCalibData.py
3.	m02_Calibration.py
4.	m03_TestStateDetection.py
5.	m04_TestStateDetectionGUI.py
6.	m96_visualization.py
7.	m97_sensorCom.py
8.	m98_magMapEval.py
9.	m99_BfieldSimulation.py
Files m96-m99 provide functions for sensor communication, B-field computation, visualization and evaluation of the magnetic map and will not be discussed in this summary.
WARNING: For some unknown reason the communication between PC and uC freezes once in a while, the sensor output will remain constant. In this case kill the script, disconnect the joystick from the PC and reconnect.
Dependencies: 

•	numpy
•	scipy version 1.3+ (subpackge optimize the differential_evolution code)
•	pyserial
•	magpylib v2.2.0+ (included in the folder)
•	tkinter (for visualization only)


Calibration and Test
To calibrate and test the system follow the steps below:
Step1:
Set the correct paths in m00 (relative to the location of the python files). The folder where all calibration data files are stored must be created by hand.

Step2:
Run the script m01. This script will store the user calibration data. The user is required to move the joystick to different, designated positions. There are four rotation positions rot1,rot2,rot3,rot4 that are indicated on the system knob and five tilt positions: 
•	tilt0 = center
•	tilt1 = towards uC
•	tilt2 = to the right (uC pointing to you)
•	tilt3 = away from uC
•	tilt4 = to the left (uC pointing to you)
Perform the following steps:
1.	Rotate to start position = rot1 and tilt0 (let go of joystick)
2.	Start script - this will store [rot1,tilt0]
3.	Tilt to all four positions (first 1, then 2, then 3, then 4). Hold each position until screen output tells you to continue to the next one.
4.	When all five states are stored go to tilt0 (let go of joystick) and rotate to rot2 as demanded by the screen output.
5.	Continue like this until all 20 states are stored, at which point the script will automatically exit.

Step3:
Run script m02. Follow the output (mean squared badness value). It should be less than 0.01 in the end. If this is not the case the system might not be very well calibrated. Possible reasons:
1.	The algorithm might have failed (rerun the script, check convergence behavior, increase popsize or maxiter, reduce tol).
2.	The calibration data is bad: repeat Step 2 then rerun m02.
3.	The system might be bad mechanically.

Step4:
The system is now calibrated. 
Run m03/m04 to test the calibration. This will generate a look-up table with N=72 states per circle (this will work fast with the uC) and will generate a console/graphical output of the form [TILT,ROT] based on this look-up table.
Algorithmic measures have been taken to generate a “nice” output:
1.	A threshold defines how close one must be to a state to register it.
2.	There is an undefined state [999,999] when in-between tilt states when one is above the threshold for all states. This state is not displayed.
3.	Neighboring ROT states are not displayed to avoid flickering
These are some simple measures that can further be improved upon. Specifically, there are multiple thresholds throughout the code that are explained in the code which can be tuned to improve usability.
