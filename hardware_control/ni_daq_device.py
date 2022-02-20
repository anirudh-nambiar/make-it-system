import nidaqmx
import time

"""
Example code showing how to communicate with NI DAQ devices.
Hardware: DAQ device
Manufacturer: National Instruments
Documentation: https://nidaqmx-python.readthedocs.io/en/latest/index.html#
Notes:
	Requires NI-DAQmx driver to be installed on computer.
	See documentation for further applications.
"""

# Device names (can be found in NI MAX interface)
# Other name examples: 'cDAQ9184-1BD49D8Mod1'
analog_device = 'Dev1'
digital_device = 'Dev2'

# ------------- Create analog input channel -------------

# Example use case: read an analog voltage signal from a transducer (that senses pressure, for instance)

ai_task = nidaqmx.Task()
ai_task.ai_channels.add_ai_voltage_chan(analog_device+"/ai0") # add ai channel 0 (can be changed)
val = ai_task.read() # read voltage signal, can be converted to physical quantity of interest (e.g., pressure) through calibration

# ------------- Create digital output channel -------------

# Example use case: turn a relay on/off

do_task = nidaqmx.Task()
do_task.do_channels.add_do_chan(digital_device+'/port0/line0') # add port 0 line 0 (can be changed)
do_task.write(True) # digital on
do_task.write(False) # digital off
val = do_task.read() # read current status