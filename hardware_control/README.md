## Description

This folder contains Python classes developed to interface with common lab equipment for chemical synthesis.

Each Python file contains information regarding the hardware model, manufacturer, and setup. See the end of each file for example code to test hardware control.
Manuals for the various equipment are compiled in the `manuals` folder. This is unofficial code and we are not affiliated with any of the equipment manufacturers.

Code was tested using Python version 3.5.

## Equipment with Serial Communication Interface

Required Python packages:
- pySerial (installation commands: `pip install pyserial` or `conda install pyserial`)

The following hardware classes utilize the serial communication protocol:
- `alicat_pressure_controller.py`: control the pressure setpoint of an Alicat pressure controller
- `rheodyne_valve.py`: control the position of a Rheodyne selector valve
- `robot_control_gui.py`: control a Newmark Systems Cartesian robot and Robotiq 2-finger gripper with a GUI built using the tkinter Python package
- `vici_pump.py`: set the flow rate of a VICI M Series positive displacement pump
- `vici_valve.py`: actuate a VICI HPLC sample injection valve

Note: The robot control GUI also requires the tkinter and crcmod Python packages.

## Agilent HPLC ChemStation Control

