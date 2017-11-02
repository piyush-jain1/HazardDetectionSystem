import serial

ser = serial.Serial(
    port='/dev/ttyUSB2',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)

#this will store the line
line = []
flag = 0
ser.write("0")
while True:
	for c in ser.read():
		line.append(c)
		if c == '\n':
			str1=''.join(line)
			print("line is : " + str1)
			line = str1.split()
			temperature = float(line[0])
			vibration = float(line[1])
			gas = float(line[2])
			if(temperature >= 27.0):
				ser.write("1")
				flag = 1
			elif(vibration > 3.0):
				ser.write("2")
				flag = 1
			elif(gas >= 250.0):
				ser.write("3")
				flag = 1
			if (flag == 0):
				ser.write("0")
			flag = 0
			with open("./hazard.txt","a+") as output:
				output.write(str1+"\n")
			line = []
			break

ser.close()
