# Mini Controler

The application kit contains :

* Mini controller with 4 tilt directions and 360° rotation.
* The Infineon XENSIV(TM) 3D Magnetic Sensor 2GO kit


<p float="left">
  <img src="https://www.infineon.com/export/sites/default/media/products/Sensors/3D-Magnetic-Sensor2GO_TLC1930-W286_Board_and_Button.jpg_422899829.jpg" width="200" />
  <img src="https://www.infineon.com/export/sites/default/media/products/Sensors/3D-Magnetic-Sensor2GO_TLC1930-W286_Button.jpg_824455825.jpg" width="200" /> 
</p>

The Mini controller is a joystick with five tilt positions as well as a 360° knob rotation. The principle idea is to detect all motion degrees by combining a single magnet with one 3D magnetic field sensor. 

Code summary: The Mini Control code contains the following files:
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


## Dependencies: 

```bash
pip install {lib}

```
*	numpy
*	scipy version 1.3+ (subpackge optimize the differential_evolution code)
*	pyserial
*	magpylib v2.2.0+ (included in the folder)
*	tkinter (for visualization only)
* bitstring

## Calibration and Test
To calibrate and test the system follow the steps below:

### Step1:
This step is to be performed only on the first use of the uC. The Firmware needs to be flashed into the uC. The Firmware is located on the folder FW. Run flash.bat to flash the uC.

### Step2:
Run the script m01. This script will store the user calibration data. The user is required to move the joystick to different, designated positions. There are four rotation positions that are indicated on the system knob and five tilt positions: 

Perform the following steps:
1.	Rotate to start position (Forward)
2.	Start script 
3.	Tilt to all four positions (first 1, then 2, then 3, then 4). Hold each position until screen output tells you to continue to the next one.
4.	When all five states are stored go to tilt0 (Center) and rotate to the next position as demanded by the screen output.
5.	Continue like this until all 20 states are stored, at which point the script will automatically exit.

### Step3:
Run script m02. Follow the output (mean squared badness value). It should be less than 0.01 in the end. If this is not the case the system might not be very well calibrated. Possible reasons:
1.	The algorithm might have failed (rerun the script, check convergence behavior, increase popsize or maxiter, reduce tol).
2.	The calibration data is bad: repeat Step 2 then rerun m02.
3.	The system might be bad mechanically.

### Step4:
The system is now calibrated. 
Run m03/m04 to test the calibration. This will generate a look-up table with N=360 states per circle (this will work fast with the uC) and will generate a console/graphical output of the form [TILT,ROT] based on this look-up table.
Algorithmic measures have been taken to generate a “nice” output:

