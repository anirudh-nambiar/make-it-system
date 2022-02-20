# Gantry Robot and Gripper Control Simple GUI
# Date: 10/17/2019
# Author: Tim Kulesza

# ---------- Gantry robot ----------

# Manufacturer: Newmark Systems Inc.
# Description: 3 linear XYZ axes (DS series linear stages), 1 theta axis (RM-8 series rotary stage)
# Controller: NSC-G4-X2 stepper motor controller
# Manual: https://www.newmarksystems.com/motion-controllers/nsc-g-series/
# Communication protocol: RS-232 (serial)

# ------------ Gripper -------------

# Manufacturer: Robotiq Inc.
# Model: 2-Finger 85 mm Adaptive Gripper
# Website: https://robotiq.com/products/2f85-140-adaptive-robot-gripper
# Manual: https://assets.robotiq.com/website-assets/support_documents/document/2F-85_2F-140_Instruction_Manual_e-Series_PDF_20190206.pdf
# Communication protocol: RS-232 (serial)


import tkinter
import serial
import time
import crcmod.predefined
import binascii
from tkinter import *

# Serial object for robot
ser=serial.Serial()
ser.baudrate=19200
ser.port='COM6' # specify COM port for robot
ser.timeout=1
ser.open()

# Serial object for gripper
ser2=serial.Serial()
ser2.baudrate=115200
ser2.port='COM35' # specify COM port for gripper
ser2.timeout=10
ser2.open()

# Gripper commands
# This line homes gripper part 1
activateclear=b'\x09\x10\x03\xe8\x00\x03\x06\x00\x00\x00\x00\x00\x00\x73\x30'
ser2.write(activateclear)
time.sleep(.01)

#This line homes gripper part 2
activate=b'\x09\x10\x03\xe8\x00\x03\x06\x01\x00\x00\x00\x00\x00\x72\xe1'
ser2.write(activate)
time.sleep(.01)

#closegrip=b'\x09\x10\x03\xe8\x00\x03\x06\x09\x00\x00\xff\xff\xff\x42\x29'
opengrip=b'\x09\x10\x03\xe8\x00\x03\x06\x09\x00\x00\x00\x05\xff\x30\xb9'
closegriphalf=b'\x09\x10\x03\xe8\x00\x03\x06\x09\x00\x00\xff\x0f\x7f\x07\x89' # close gripper half speed
closegripfull=b'\x09\x10\x03\xe8\x00\x03\x06\x09\x00\x00\xff\x0f\xff\x06\x29' # close gripper full speed

# Gantry commands
homecom='XQ#HOME;'
stop='ST ABCD;'

xup='PR 10000; BGA;'
xdown='PR -10000; BGA;'
yup='PR ,10000; BGB;'
ydown='PR ,10000; BGB;'
zup='PR ,,10000; BGC;'
zdown='PR ,,10000; BGC;'
thetaup='PR ,,,10000; BGD;'
thetadown='PR ,,,10000; BGD;'

xjogpos='JG 100000; BGA;'
xjogneg='JG -100000; BGA;'
yjogpos='JG ,100000; BGB;'
yjogneg='JG ,-100000; BGB;'
zjogpos='JG ,,100000; BGC;'
zjogneg='JG ,,-100000; BGC;'
thetajogpos='JG ,,,180000; BGD;'
thetajogneg='JG ,,,-180000; BGD;'

speeddefault='SP 10000, 10000, 10000, 10000;'
speedslow='SP 50000, 50000, 50000, 50000;'
accdefault='AC 250000, 250000, 250000, 250000;'
dcdefault='DC 250000, 250000, 250000, 250000;'

homeposition='622265, 416451, 0, 0'
storageposition='653753, 369711, 555468, -2042477'

ser.write(accdefault.encode('ASCII'))
ser.write(dcdefault.encode('ASCII'))
time.sleep(1)


# Code to create GUI
top=Tk()
top.title('Robot Control Panel')
top.geometry('600x600')
top.maxsize(600,600)
top.minsize(600,600)
leftframe=Frame(top)
rightframe=Frame(top)
bottomframe=Frame(top)
topframe=Frame(top)
topframe.pack(side=TOP)
leftframe.pack(side=LEFT)
rightframe.pack(side=RIGHT)
bottomframe.pack(side=BOTTOM)

resscale=Scale(topframe, from_=10, to=10000, label="Step Resolution")
resscale.set(10000)
resscale.pack(side=LEFT)

jogval=IntVar()
jogval.set(1)


# Commands to control system
def xleft(event):
	if jogval.get()==1:
		ser.write(speeddefault.encode('ASCII'))
		print('jogging x neg')
		ser.write(xjogpos.encode('ASCII'))
		
	else:
		speedraw=int(resscale.get()*2.5)
		newspeed=str(speedraw)
		speedcommand='SP '+newspeed+', '+newspeed+', '+newspeed+', '+newspeed+';'
		ser.write(speedcommand.encode('ASCII'))
		rescommand='PR '+str(resscale.get())+'; BGA;'
		print('stepping')
		ser.write(rescommand.encode('ASCII'))
	
def xright(event):
	if jogval.get()==1:
		ser.write(speeddefault.encode('ASCII'))
		print('jogging x pos')
		ser.write(xjogneg.encode('ASCII'))
	else:
		speedraw=int(resscale.get()*2.5)
		newspeed=str(speedraw)
		speedcommand='SP '+newspeed+', '+newspeed+', '+newspeed+', '+newspeed+';'
		ser.write(speedcommand.encode('ASCII'))
		rescommand='PR -'+str(resscale.get())+'; BGA;'
		print('stepping')
		ser.write(rescommand.encode('ASCII'))
		
def yup(event):
	if jogval.get()==1:
		ser.write(speeddefault.encode('ASCII'))
		print('jogging y pos')
		ser.write(yjogneg.encode('ASCII'))
	else:
		speedraw=int(resscale.get()*2.5)
		newspeed=str(speedraw)
		speedcommand='SP '+newspeed+', '+newspeed+', '+newspeed+', '+newspeed+';'
		ser.write(speedcommand.encode('ASCII'))
		rescommand='PR ,-'+str(resscale.get())+'; BGB;'
		print('stepping')
		ser.write(rescommand.encode('ASCII')) 
	  
def ydown(event):   
	if jogval.get()==1:
		ser.write(speeddefault.encode('ASCII'))
		print('jogging y neg')
		ser.write(yjogpos.encode('ASCII'))
	else:
		speedraw=int(resscale.get()*2.5)
		newspeed=str(speedraw)
		speedcommand='SP '+newspeed+', '+newspeed+', '+newspeed+', '+newspeed+';'
		ser.write(speedcommand.encode('ASCII'))
		rescommand='PR ,'+str(resscale.get())+'; BGB;'
		print('stepping')
		ser.write(rescommand.encode('ASCII')) 
	
def zup(event):
	if jogval.get()==1:
		ser.write(speeddefault.encode('ASCII'))
		print('jogging z pos')
		ser.write(zjogpos.encode('ASCII'))
	else:
		speedraw=int(resscale.get()*2.5)
		newspeed=str(speedraw)
		speedcommand='SP '+newspeed+', '+newspeed+', '+newspeed+', '+newspeed+';'
		ser.write(speedcommand.encode('ASCII'))
		rescommand='PR ,,'+str(resscale.get())+'; BGC;'
		print('stepping')
		ser.write(rescommand.encode('ASCII'))
	
def zdown(event):
	if jogval.get()==1:
		ser.write(speeddefault.encode('ASCII'))
		print('jogging z neg')
		ser.write(zjogneg.encode('ASCII')) 
	else:
		speedraw=int(resscale.get()*2.5)
		newspeed=str(speedraw)
		speedcommand='SP '+newspeed+', '+newspeed+', '+newspeed+', '+newspeed+';'
		ser.write(speedcommand.encode('ASCII'))
		rescommand='PR ,,-'+str(resscale.get())+'; BGC;'
		print('stepping')
		ser.write(rescommand.encode('ASCII'))

def tup(event):
	if jogval.get()==1:
		ser.write(speeddefault.encode('ASCII'))
		print('jogging t pos')
		ser.write(thetajogpos.encode('ASCII'))
	else:
		speedraw=int(resscale.get()*2.5)
		newspeed=str(speedraw)
		speedcommand='SP '+newspeed+', '+newspeed+', '+newspeed+', '+newspeed+';'
		ser.write(speedcommand.encode('ASCII'))
		rescommand='PR ,,,'+str(resscale.get())+'; BGD;'
		print('stepping')
		ser.write(rescommand.encode('ASCII'))
	
def tdown(event):
	if jogval.get()==1:
		ser.write(speeddefault.encode('ASCII'))
		print('jogging t neg')
		ser.write(thetajogneg.encode('ASCII'))
	else:
		speedraw=int(resscale.get()*2.5)
		newspeed=str(speedraw)
		speedcommand='SP '+newspeed+', '+newspeed+', '+newspeed+', '+newspeed+';'
		ser.write(speedcommand.encode('ASCII'))
		rescommand='PR ,,,-'+str(resscale.get())+'; BGD;'
		print('stepping')
		ser.write(rescommand.encode('ASCII'))
	   
def stopbut(event):         
	print('stop')
	ser.write(stop.encode('ASCII'))
	
def emergstop():
	print('emergency stop')
	ser.write(stop.encode('ASCII'))

def opengripper():
	ser2.write(opengrip)

def closegripper():
	ser2.write(closegripfull)

def closeslow():
	ser2.write(closegriphalf)  

def clickandclose():
	global gripflag
	ser2.read_all()
	#time.sleep(.1)
	readpos=b'\x09\x03\x07\xd2\x00\x01\x24\x0f'
	ser2.write(readpos)
	time.sleep(.1)
	posraw=ser2.read_all()
	grippos=binascii.hexlify(posraw)
	targetgrippos=int(grippos[6:8], 16)+3
	print(targetgrippos)
	#print(int(grippos[6:8], 16))
	targetgripposhex=hex(targetgrippos).lstrip("0x")
	#print(targetgripposhex)

	if len(targetgripposhex)==1:
		targetstring='091003e80003060900000'+targetgripposhex+'0fff'
	else:
		targetstring='091003e8000306090000'+targetgripposhex+'0fff'

	crc16=crcmod.predefined.Crc('modbus')
	crc16.update(binascii.unhexlify(targetstring))
	crcstring=str(crc16.hexdigest())
	#print(crcstring)
	targetstringfinal=targetstring+crcstring[2:4]+crcstring[0:2]
	#print(targetstringfinal)
	ser2.write(binascii.unhexlify(targetstringfinal))
	gripflag=bottomframe.after(100, lambda:clickandclose())

def clickandopen():
	global gripflag
	ser2.read_all()
	#time.sleep(.1)
	readpos=b'\x09\x03\x07\xd2\x00\x01\x24\x0f'
	ser2.write(readpos)
	time.sleep(.1)
	posraw=ser2.read_all()
	grippos=binascii.hexlify(posraw)
	#print(posraw)
	#print(grippos)
	
	targetgrippos=int(grippos[6:8], 16)-3
	#print(int(grippos[6:8], 16))
	targetgripposhex=hex(targetgrippos).lstrip("0x")
	#print(targetgripposhex)

	if len(targetgripposhex)==1:
		targetstring='091003e80003060900000'+targetgripposhex+'0f7f'
	else:
		targetstring='091003e8000306090000'+targetgripposhex+'0f7f'
	
	crc16=crcmod.predefined.Crc('modbus')
	crc16.update(binascii.unhexlify(targetstring))
	crcstring=str(crc16.hexdigest())
	#print(crcstring)
	targetstringfinal=targetstring+crcstring[2:4]+crcstring[0:2]
	#print(targetstringfinal)
	ser2.write(binascii.unhexlify(targetstringfinal))
	gripflag=bottomframe.after(100, lambda:clickandopen())
	  
def startclose():
	#print('Starting to close')
	clickandclose()
	
def startopen():
	#print('Starting to open')
	clickandopen()
	
def stopclose():
	global gripflag
	#print('Stopping closing')
	#print(gripflag)
	bottomframe.after_cancel(gripflag)

def stopopen():
	global gripflag
	#print('Stopping opening')
	bottomframe.after_cancel(gripflag)

def gotozero():
	ser.write(speeddefault.encode('ASCII'))
	command='PA 0,0,0,0; BG;'
	ser.write(command.encode('ASCII'))

def gotopos():
	ser.write(speeddefault.encode('ASCII'))
	command='PA '+ posentry.get() + '; BG;'
	ser.write(command.encode('ASCII'))
	print(command)
	
def getpos():
	ser.read_all()
	time.sleep(.1)
	command='RP;'
	ser.write(command.encode('ASCII'))
	time.sleep(.1)
	# response=ser.read_until(terminator=b'\r')
	response=ser.read_until(expected=b'\r')
	#print(response)
	# print(response)
	print(response.decode('ASCII'))
	#print(command)
	poslabeltext=StringVar()
	poslabeltext.set(response.decode('ASCII'))
	#poslabel.config(text=response.decode('ASCII'))
	poslabel.config(textvariable=poslabeltext)

def homegantry():
	# This line sends robot to home position
	# Robot must be homed each time control box is turned off and on
	ser.write(homecom.encode('ASCII'))
	print('homing (wait for robot to stop moving)')
	

# Create GUI elements
btnleft=Button(leftframe, text="Left")
btnleft.bind('<Button-1>', xleft)
btnleft.bind('<ButtonRelease-1>', stopbut)

btnright=Button(leftframe, text="Right")
btnright.bind('<Button-1>', xright)
btnright.bind('<ButtonRelease-1>', stopbut)

btntop=Button(leftframe, text="Up")
btntop.bind('<Button-1>', yup)
btntop.bind('<ButtonRelease-1>', stopbut)

btndown=Button(leftframe, text="Down")
btndown.bind('<Button-1>', ydown)
btndown.bind('<ButtonRelease-1>', stopbut)

btnstop=Button(topframe, text="Emergency Stop", bg='red', command=lambda: emergstop())
btnhome=Button(topframe, text="Home Gantry", bg='green', command=lambda: homegantry())

btnleft2=Button(rightframe, text="Theta (-)")
btnleft2.bind('<Button-1>', tdown)
btnleft2.bind('<ButtonRelease-1>', stopbut)

btnright2=Button(rightframe, text="Theta (+)")
btnright2.bind('<Button-1>', tup)
btnright2.bind('<ButtonRelease-1>', stopbut)

btntop2=Button(rightframe, text="Z Up")
btntop2.bind('<Button-1>', zup)
btntop2.bind('<ButtonRelease-1>', stopbut)

btndown2=Button(rightframe, text="Z Down")
btndown2.bind('<Button-1>', zdown)
btndown2.bind('<ButtonRelease-1>', stopbut)

btntop.pack(side = TOP)
btnleft.pack(side = LEFT)
btnright.pack(side = RIGHT)
btndown.pack(side=BOTTOM)
btntop2.pack(side = TOP)
btnleft2.pack(side = LEFT)
btnright2.pack(side = RIGHT)
btndown2.pack(side=BOTTOM)

btnstop.pack(side=LEFT)
btnhome.pack(side=LEFT)

r1=Radiobutton(topframe, text="Jogging", variable=jogval, value=1)
r2=Radiobutton(topframe, text="Steps", variable=jogval, value=2)
r1.pack(side=LEFT)
r2.pack(side=LEFT)

btnopen=Button(bottomframe, text="Open", command=lambda: opengripper())
btnclose=Button(bottomframe, text="Close Gripper Full Force", command=lambda: closegripper())
btncloseslow=Button(bottomframe, text="Close Gripper Half Force", command=lambda: closeslow())
btnclickandclose=Button(bottomframe, text="Click and Close")
btnclickandclose.bind('<Button-1>', lambda event: startclose())
btnclickandclose.bind('<ButtonRelease-1>', lambda event: stopclose())
btnclickandopen=Button(bottomframe, text="Click and Open")
btnclickandopen.bind('<Button-1>', lambda event: startopen())
btnclickandopen.bind('<ButtonRelease-1>', lambda event: stopopen())

btnopen.pack(side=TOP)
btnclose.pack(side=TOP)
btncloseslow.pack(side=TOP)
btnclickandclose.pack(side=TOP)
btnclickandopen.pack(side=TOP)
btngotozero=Button(bottomframe, text="Go to Zero", command=lambda: gotozero())
btngotopos=Button(bottomframe, text="Go to Position", command=lambda: gotopos())
btngetpos=Button(bottomframe, text="Get Position", command=lambda: getpos())
posentry=Entry(bottomframe, width=50)
poslabel=Entry(bottomframe, width=50, state='readonly', readonlybackground='white', fg='black')

btngotozero.pack(side=TOP)
btngotopos.pack(side=TOP)
btngetpos.pack(side=TOP)
posentry.pack(side=TOP)
poslabel.pack(side=TOP, pady=(0,10))


top.mainloop() # launches GUI