import serial
import time

class AlicatPressureController:
	
	"""
	Hardware: Pressure controller (PCD series)
	Manufacturer: Alicat Scientific
	Website: https://www.alicat.com/models/pcd-dual-valve-absolute-and-gauge-pressure-controllers/
	Manual: https://documents.alicat.com/manuals/DOC-MANUAL-9V-PCD.pdf
	Communication protocol: RS-232 (serial)
	Notes:
		Ensure setpoint source is set to Serial/Front Panel on controller.
	"""
	
	def __init__(self, port, baud=19200, timeout=2):
		"""
		Args:
			port (str): COM port (example: 'COM30')
			baud (int): baud rate (default is 19200 for controller)
			timeout (float): read timeout value in seconds
		"""
		self.port = port
		self.baud = baud
		self.timeout = timeout
		self.ser = serial.Serial(port, baud, timeout=timeout)

	def send_msg(self, msg):
		msg = msg.encode('utf-8')
		self.ser.write(msg)

	def set_pressure(self, unit_id, pressure):
		"""
		Args:
			unit_id (str): unit id for controller (default is 'A')
			pressure (float): pressure setpoint in selected units (usually psi)
		"""
		command = '{}S{}\r'.format(unit_id, pressure) # example: 'AS10'
		self.send_msg(command)
		print('Pressure set to {}'.format(pressure))

	def stop(self):
		self.ser.close()
		print('Disconnected from {}'.format(self.__class__.__name__))


# Code to test hardware control
if __name__ == '__main__':
	
	# Connect
	port = 'COM30'
	alicat = AlicatPressureController(port)
	
	# Control
	unit_id = 'A'
	pressure = 10
	alicat.set_pressure(unit_id, pressure)
	
	# Disconnect
	alicat.stop()