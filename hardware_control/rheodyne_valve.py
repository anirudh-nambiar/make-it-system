import serial
import time

class RheodyneValve:

	"""
	Hardware: Rheodyne selector valve (24-position)
	Manufacturer: Rheodyne (now IDEX Health & Science)
	Manual: https://www.idex-hs.com/wp-content/uploads/2018/05/UART-USB-Communication-Protocol-for-TitanEX.pdf.zip
	Communication protocol: RS-232 (serial)
	Notes:
		Code tested with Rheodyne valve model PD2425-925.
	"""
	
	def __init__(self, port, baud=19200, timeout=2):
		"""
		Args:
			port (str): COM port (example: 'COM30')
			baud (int): baud rate (default is 19200 for valve)
			timeout (float): read timeout value in seconds
		"""
		self.port = port
		self.baud = baud
		self.timeout = timeout
		self.ser = serial.Serial(port, baud, timeout=timeout)

	def send_msg(self, msg):
		msg = msg.encode('utf-8')
		self.ser.write(msg)

	def set_position(self, position):
		"""Go to specified position.
		Args:
			position (int): position between 1-24 for 24-position valve
		"""
		command = 'P{:02X}\r'.format(int(position))
		self.send_msg(command)
		print('Rheodyne valve set to position {}'.format(int(position)))

	def stop(self):
		self.ser.close()
		print('Disconnected from {}'.format(self.__class__.__name__))


# Code to test hardware control
if __name__ == '__main__':
	
	# Connect
	port = 'COM30'
	rheo = RheodyneValve(port)
	
	# Control
	rheo.set_position(2)
	time.sleep(2)
	rheo.set_position(1)
	
	# Disconnect
	rheo.stop()