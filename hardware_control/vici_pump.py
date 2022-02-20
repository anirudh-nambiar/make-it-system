import serial
import time

class VICIPump:

	"""
	Hardware: Cheminert M Series pump
	Manufacturer: VICI Valco Instruments
	Website: https://www.vici.com/liqhand/m6.php
	Manual: https://www.vici.com/support/manuals/m6-m50.MForce.pdf
	Communication protocol: RS-422/485 (serial)
	Notes:
		Multiple pumps can be daisy chained and controlled using a single COM port using party mode (see manual).
		Pumps can be connected to the computer separately too.
	"""
	
	def __init__(self, port, baud=9600, timeout=2):
		"""
		Args:
			port (str): COM port (example: 'COM30')
			baud (int): baud rate (default is 9600 for pump)
			timeout (float): read timeout value in seconds
		"""
		self.port = port
		self.baud = baud
		self.timeout = timeout
		self.ser = serial.Serial(port, baud, timeout=timeout)

	def send_msg(self, msg):
		msg = msg.encode('utf-8')
		self.ser.write(msg)

	def set_flow(self, fr_mL_min, uL_rev=100, addr=''):
		"""
		Set pump flow rate.
		Args:
			fr_mL_min (float): Flow rate in mL/min (milliliters/minute)
			uL_rev (float): Microliters per revolution. Default values for pump models: 100 uL/rev (Model M6), 628 uL/rev (Model M50).
			addr (int/str): Pump address required when using party mode. Can be single ASCII character from a-z, A-Z, or 0-9.
		"""
		fr_uL_s = fr_mL_min*1000/60 # convert flow rate from mL/min to uL/s
		factor = 256*200*9.8596/float(uL_rev)*float(fr_uL_s) # numbers related to stepper motor parameters
		command = '\n%sSL=%d\r\n' % (addr, int(factor)) # examples: 'SL=1000', 'aSL=1000' (party mode)
		self.send_msg(command)

	def stop_flow(self, addr=''):
		"""
		Stop pump flow.
		Args:
			addr (int/str): Pump address required when using party mode. Can be single ASCII character from a-z, A-Z, or 0-9.
		"""
		self.set_flow(0, addr=addr)

	def check_version(self, addr=''):
		"""
		Check firmware version of MForce controller.
		Args:
			addr (int/str): Pump address required when using party mode. Can be single ASCII character from a-z, A-Z, or 0-9.
		"""
		addr = str(addr)
		command = '%sPR VR\r\n' % addr
		self.send_msg(command)
	
	def set_address(self, addr, current=''):
		"""
		Set and save address when using party mode.
		Args:
			addr (int/str): Address to set pump to when using party mode. Can be single ASCII character from a-z, A-Z, or 0-9.
			current (int/str): Address pump is currently set to. Can be single ASCII character from a-z, A-Z, or 0-9.
		"""
		self.send_msg('\n%sDN="%s"\r' % (current, str(addr))) # set address
		self.send_msg('\n%sS\r\n' % addr) # save address
	
	def set_party(self, party):
		"""
		Enable(1) or disable(0) party mode.
		Args:
			party (int): Enable(1) or disable(0)
		"""
		self.send_msg('\rPY=%d\r\n' % int(party))

	def stop(self):
		self.ser.close()
		print('Disconnected from {}'.format(self.__class__.__name__))


# Code to test hardware control
if __name__ == '__main__':
	
	# Connect
	port = 'COM30'
	vici = VICIPump(port)
	
	# Control
	fr = 0.1 # mL/min
	vici.set_flow(fr)
	time.sleep(5)
	vici.stop_flow()
	
	# Disconnect
	vici.stop()