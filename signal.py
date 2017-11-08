import serial
import time

ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)

temp_wait = 0
gas_wait = 0
vibration_wait = 0
fire_active = 0
gas_active = 0
earthquake_active  = 0

#this will store the line
line = []
flag = 0
ser.write("0")
start = time.time()
while True:
	if(temp_wait or vibration_wait or gas_wait):
		if(time.time()-start>=0.5):
			temp_wait = 0
			vibration_wait = 0
			gas_wait = 0
	file = open("userpref.txt", "r")
	pref = file.readline()
	#print pref
	if len(pref) > 0 : 
		sett = pref.split()
		#print "sett[0] :" , sett[0]
		if(sett[0] == '0'):
			fire_active = 0 
		else: 
			fire_active  = 1
		#print "sett[1] :" , sett[1]
		if(sett[1] == '0'):
			earthquake_active = 0
		else:
			earthquake_active = 1
		#print "sett[2] :" , sett[2]
		if(sett[2] == '0'):
			gas_active = 0
		else:
			gas_active = 1
	for c in ser.read():
		line.append(c)
		if c == '\n':
			str1=''.join(line)
			print("line is : " + str1)
			line = str1.split()
			temperature = float(line[0])
			vibration = float(line[1])
			gas = float(line[2])
			with open("./temp_reading.txt", "w+") as output:
				output.write(str(temperature))
			if(temp_wait or vibration_wait or gas_wait):
				ser.write("0")
			else:
				if(temperature >= 27.0 and fire_active == 1):
					ser.write("1")
					flag = 1
					start = time.time()
					temp_wait = 1
				elif(vibration > 3.0 and earthquake_active == 1):
					ser.write("2")
					start = time.time()
					flag = 1
					vibration_wait = 1
				elif(gas >= 250.0 and gas_active == 1):
					ser.write("3")
					flag = 1
					start = time.time()
					gas_wait = 1
				if (flag == 0 ):
					ser.write("0")
				flag = 0
			with open("./hazard.txt","a+") as output:
				output.write(str1+"\n")
			line = []
			break
ser.close()
