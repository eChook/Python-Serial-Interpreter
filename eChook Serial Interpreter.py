from serial import *
from tkinter import *
from time import sleep

#make a TkInter Window
root = Tk()
root.wm_title("eChook Serial Interpreter")


#Varialbes to Read In
voltage = 0
voltageLower = 0
current = 0
throttle = 0
temp1 = 0
temp2 = 0
brake = 0
button1 = 0
button2 = 0
motorRPM = 0
wheelSpeed = 0

voltageString = StringVar()
voltageLowerString  = StringVar()
throttleString = StringVar()
currentString = StringVar()
motorRPMString = StringVar()
wheelSpeedString = StringVar()
temp1String = StringVar()
temp2String = StringVar()
brakeString = StringVar()
button1String = StringVar()
button2String = StringVar()
motorRPMString = StringVar()
wheelSpeedString = StringVar()

userPort = StringVar()

ser = Serial()

connectButtonText = StringVar()
connectButtonText.set("Connect")

serBuffer = []

def serialConnect():
	if not ser.is_open:
		
		port = "\\\\.\\COM"+userPort.get()
		#print (port)
		ser.baudrate = 115200
		ser.port = port
		ser.timeout = 0
		ser.writeTimeout = 0
		ser.open()
		sleep(0.01)
		if ser.is_open:
			connectButtonText.set("Disonnect")	
		root.after(100, readSerial)				
	elif ser.is_open:
		ser.close()
		connectButtonText.set("Connect")



def readSerial():
    while ser.is_open:
        c = ser.read() # attempt to read a character from Serial
                
        #was anything read?
        if len(c) == 0:
            break

        # get the buffer from outside of this function
        global serBuffer
                
        serBuffer.append(c)

        if(len(serBuffer) > 5 ):

        	if(ord(serBuffer[len(serBuffer)-1]) == 125 and ord(serBuffer[len(serBuffer)-5]) == 123 ):
        		identifier = serBuffer[len(serBuffer)-4]
	        	upperByte = serBuffer[len(serBuffer)-3]
	        	lowerByte = serBuffer[len(serBuffer)-2]
	        	assignByID(identifier, decode(upperByte,lowerByte))
	        	del serBuffer[:len(serBuffer)-5]
        	
    
    root.after(10, readSerial) # check serial again soon

def decode(upperByte, lowerByte):
	upperByte = ord(upperByte)
	lowerByte = ord(lowerByte)

	if(upperByte == 255 & lowerByte == 255):
		return 0
	elif (upperByte > 127): #indicates a value of over 127 is being sent, therefore an integer value
		hundreds = (upperByte - 128)*100
		if(upperByte == 255):
			hundreds = 0
		tens = lowerByte
		if(lowerByte == 255):
			tens = 0
		return hundreds + tens
	else:
		intValue = upperByte
		if(upperByte == 255):
			intValue = 0
		decimal = float(lowerByte/100)
		if(lowerByte == 255):
			decimal = 0
		return intValue + decimal

def assignByID(identifier, value):
	global voltage
	global voltageString
	global voltageLower
	global voltageLowerString
	global current
	global currentString
	global throttle
	global throttleString
	global temp1
	global temp1String
	global temp2
	global temp2String
	global brake
	global brakeString
	global button1
	global button1String
	global button2
	global button2String
	global motorRPM
	global motorRPMString
	global wheelSpeed
	global wheelSpeedString

	identifier = chr(ord(identifier))

	if(identifier == 'i'):
		current = value
		print("Current = " + str(value))
		currentString.set("{0:.2f}".format(value)+"A")
	elif(identifier == 'v'):
		voltage = value
		print("Voltage = " + str(value))
		voltageString.set("{0:.2f}".format(value)+"V")
	elif(identifier == 't'):
		throttle = value
		print("Throttle = " + str(value))
		throttleString.set("{0:.2f}".format(value)+"%")
	elif(identifier == 'a'):
		temp1 = value
		print("Temp1 = " + str(value))
		temp1String.set("{0:.2f}".format(value)+"°C")
	elif(identifier == 'b'):
		temp2 = value
		print("Temp2 = " + str(value))
		temp2String.set("{0:.2f}".format(value)+"°C")
	elif(identifier == 'w'):
		voltageLower = value
		print("Voltage Lower = " + str(value))
		voltageLowerString.set("{0:.2f}".format(value)+"V")
	elif(identifier == 'B'):
		brake = value
		print("Brake = " + str(value))
		brakeString.set("{0:.2f}".format(value))
	elif(identifier == 'L'):
		button1 = value
		print("Button 1 = " + str(value))
		button1String.set("{0:.2f}".format(value))
	elif(identifier == 'C'):
		button2 = value
		print("Button 2 = " + str(value))
		button2String.set("{0:.2f}".format(value))
	elif(identifier == 'm'):
		motorRPM = value
		print("Motor RPM = " + str(value))
		motorRPMString.set("{0:.2f}".format(value))
	elif(identifier == 'm'):
		wheelSpeed = value
		print("Wheel Speed = " + str(value))
		wheelSpeedString.set("{0:.2f}".format(value)+"MPH")




comLabel = Label( root, text="COM" ).grid(row=1,column=1)

connectButtonText = StringVar()
connectButtonText.set("Connect")
connectionButton = Button( root, textvariable=connectButtonText, command=serialConnect).grid(row=1, column=3)

comEntry = Entry(root,textvariable=userPort)
comEntry.grid(row=1,column=2)
comEntry.delete(0,END)
comEntry.insert(0,16)


voltageLabel = Label(root, text="Voltage = ")
voltageLabel.grid(column=1, row=2)

voltageValue = Label(root, textvariable=voltageString)
voltageValue.grid(column=2, row=2)

voltageLowerLabel = Label(root, text="Volts Low = ")
voltageLowerLabel.grid(column=1, row=3)

voltageLowerValue = Label(root, textvariable=voltageLowerString)
voltageLowerValue.grid(column=2, row=3)

currentLabel = Label(root, text="Current = ")
currentLabel.grid(column=1, row=4)

currentValue = Label(root, textvariable=currentString)
currentValue.grid(column=2, row=4)

throttleLabel = Label(root, text="Throttle = ")
throttleLabel.grid(column=1, row=5)

throttleValue = Label(root, textvariable=throttleString)
throttleValue.grid(column=2, row=5)

temp1Label = Label(root, text="Temp 1 = ")
temp1Label.grid(column=1, row=6)

temp1Value = Label(root, textvariable=temp1String)
temp1Value.grid(column=2, row=6)

temp2Label = Label(root, text="Temp 2 = ")
temp2Label.grid(column=1, row=7)

temp2Value = Label(root, textvariable=temp2String)
temp2Value.grid(column=2, row=7)

button1Label = Label(root, text="Button 1 = ")
button1Label.grid(column=1, row=8)

button1Value = Label(root, textvariable=button1String)
button1Value.grid(column=2, row=8)

button2Label = Label(root, text="Button 2 = ")
button2Label.grid(column=1, row=9)

button2Value = Label(root, textvariable=button2String)
button2Value.grid(column=2, row=9)

motorRPMLabel = Label(root, text="Motor RPM = ")
motorRPMLabel.grid(column=1, row=10)

motorRPMValue = Label(root, textvariable=motorRPMString)
motorRPMValue.grid(column=2, row=10)

wheelSpeedLabel = Label(root, text="Wheel Speed = ")
wheelSpeedLabel.grid(column=1, row=11)

wheelSpeedValue = Label(root, textvariable=wheelSpeedString)
wheelSpeedValue.grid(column=2, row=11)


root.mainloop()
