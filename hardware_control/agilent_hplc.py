import win32ui
import dde
import time

class AgilentHPLC:
	"""
	Class containing a DDE server to forward commands to ChemStation software which controls Agilent HPLCs.
	Dynamic Data Exchange (DDE) is a technology for interprocess communication used in early versions of Microsoft Windows.
	Command manual: https://www.agilent.com/cs/library/usermanuals/Public/MACROS.PDF
	Notes:
		Windows PC required for DDE.
		This script must be on the same computer as ChemStation.
		If code to control experimental platform is on a different computer,...
		one approach is to set up a socket server on the ChemStation computer that listens to requests from the platform computer.
		See manual for more commands.
	"""

	def __init__(self, chemstation_name=''):
		"""
		Args:
			chemstation_name (str): Name of ChemStation DDE client (name format: 'hpcore####').
		"""

		# Get name of ChemStation DDE client
		# Every time ChemStation software is opened, a new name is assigned
		# The code below tries to automatically find this name
		if chemstation_name == '':
			with open('C:/Chem32/1/TEMP/HPCoreLog_Acquisition.svclog') as f:
				content = f.readlines()
			anchor = content[0].rfind('ProcessID=')
			start_char = content[0].find('\"', anchor) + 1
			end_char = content[0].find('\"', start_char)
			self.chemstation_name = 'hpcore' + content[0][start_char:end_char]
		
		# If the above code fails, obtain the name manually by typing 'print _ddename$' in Chemstation command line...
		# and pass name as input argument when initiating AgilentController class
		else:
			self.chemstation_name = chemstation_name
		
		# Following code creates a DDE server that can communicate with ChemStation (which is a DDE client)
		self.server = dde.CreateServer()
		self.server.Create('AgilentController')
		self.conversation = dde.CreateConversation(self.server)
		self.conversation.ConnectTo(self.chemstation_name, 'CPWAIT')
		print('Connected to ChemStation')

	def check_status(self):
		"""Get status of HPLC. Useful for checking if HPLC is ready to run a method."""
		status = self.conversation.Request('ACQSTATUS$')
		print('Status: {}'.format(status)) # status = 'PRERUN' means HPLC is ready
		return status

	def start_method(self):
		self.conversation.Exec('StartMethod')
		time.sleep(2)
		method_on = self.conversation.Request('_METHODON')
		method_on = int(method_on)
		if method_on == 1: # 1 means method is running
			print('Success: Started HPLC method')
		else: # 0 means method is not running
			print('Error: Could not start HPLC method')
		return method_on

	def get_sample_name(self):
		"""Get sample name from most recent run. Useful for checking if exported data is available for extracting peak areas."""
		sample_name = self.conversation.Request('_DATAFILE$')
		print('Sample name: {}'.format(sample_name))
		return sample_name

	def get_method_name(self):
		"""Get name of method currently loaded."""
		method_name = self.conversation.Request('MethodName')
		print('Method name: {}'.format(method_name))
		return method_name

	def load_method(self, method_name, method_directory='C:\Chem32\1\Methods'):
		"""
		Load specified method.
		Args:
			method_name (str): Method name (example: '10_min_method'). Do not include '.M' at the end of method name, this is added by code.
			method_directory (str): Method directory. Example: 'C:\Chem32\1\Methods'
		"""
		command = r'LoadMethod "{}\", "{}.M"'.format(method_directory, method_name) # example: LoadMethod "C:\Chem32\1\Methods\", "10_min_method.M"
		self.conversation.Exec(command)

	def command_line(self):
		"""Command line interface to test ChemStation commands."""
		user_input = input("\n Type command ('test', 'start', 'status', 'getsamplename', 'getmethodname', or anything else): ")
		if user_input == "start":
			self.start_method()
		elif user_input == "status":
			self.check_status()
		elif user_input == "getsamplename":
			self.get_sample_name()
		elif user_input == "getmethodname":
			self.get_method_name()
		elif user_input == "test":
			self.conversation.Exec('print 1') # you should see "1" printed in ChemStation below command line
		else:
			user_input = str(user_input)
			self.conversation.Exec(user_input)
		self.command_line()


# Code to test hardware control
if __name__ == '__main__':

	chemstation_name = '' # leave blank if extracting automatically, else type 'print _ddename$' in Chemstation command line to get name ('hpcore####')
	agilent = AgilentHPLC(chemstation_name)
	agilent.command_line()