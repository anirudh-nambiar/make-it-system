import serial
import time

class VICIValve:

	"""
	Hardware: HPLC sample injection valve (2-position)
	Manufacturer: VICI Valco Instruments
	Website: https://www.vici.com/act/ua.php
	Manual: https://www.vici.com/support/manuals/universal-actuator.pdf
	Communication protocol: RS-232 (serial)
	"""
	
	def __init__(self, port, baud=9600, timeout=2):
		"""
		Args:
			port (str): COM port (example: 'COM30')
			baud (int): baud rate (default is 9600 for valve)
			timeout (float): read timeout value in seconds
		"""
		self.port = port
		self.baud = baud
		self.timeout = timeout
		self.ser = serial.Serial(port, baud, timeout=timeout)

	def send_msg(self, msg):
		msg = msg.encode('utf-8')
		self.ser.write(msg)

	def position_A(self):
		"""Go to position A"""
		command = 'GOA\r\n'
		self.send_msg(command)
		print('VICI valve set to position A')

	def position_B(self):
		"""Go to position B"""
		command = 'GOB\r\n'
		self.send_msg(command)
		print('VICI valve set to position B')

	def inject_ABA(self, wait_time=2):
		"""Injects sample by going from position A to B, then back to A.
		Args:
			wait_time (float): wait time in seconds before moving valve back
		"""
		self.position_B()
		time.sleep(wait_time)
		self.position_A()
		print('VICI valve ABA injection complete')

	def inject_BAB(self, wait_time=2):
		"""Injects sample by going from position B to A, then back to B.
		Args:
			wait_time (float): wait time in seconds before moving valve back
		"""
		self.position_A()
		time.sleep(wait_time)
		self.position_B()
		print('VICI valve BAB injection complete')

	def stop(self):
		self.ser.close()
		print('Disconnected from {}'.format(self.__class__.__name__))


# Code to test hardware control
if __name__ == '__main__':
	
	# Connect
	port = 'COM30'
	vici = VICIValve(port)
	
	# Control
	vici.position_B()
	time.sleep(2)
	vici.position_A()
	
	# Disconnect
	vici.stop()