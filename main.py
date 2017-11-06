from flask import Flask, request
import time
import threading

app = Flask(__name__)

# ser = serial.Serial(
#     port='/dev/ttyUSB2',\
#     baudrate=9600,\
#     parity=serial.PARITY_NONE,\
#     stopbits=serial.STOPBITS_ONE,\
#     bytesize=serial.EIGHTBITS,\
#         timeout=0)
#
# print("connected to: " + ser.portstr)

fire_detect = 1
gas_detect = 1
earthquake_detect = 1

#this will store the line
line = []
flag = 0
temp_wait = 0
gas_wait = 0
vibration_wait = 0

def func():
    global fire_detect
    global gas_detect
    global earthquake_detect
    # ser.write("0")
    while True:
        #     if(temp_wait or vibration_wait or gas_wait):
        #         time.sleep(5)
        #         temp_wait = 0
        #         vibration_wait = 0
        #         gas_wait = 0
        #     for c in ser.read():
        # 		line.append(c)
        # 		if c == '\n':
        # 			str1=''.join(line)
        # 			print("line is : " + str1)
        # 			line = str1.split()
        # 			temperature = float(line[0])
        # 			vibration = float(line[1])
        # 			gas = float(line[2])
        # 			if(temperature >= 27.0 and fire_detect):
        # 				ser.write("1")
        #                 flag = 1
        #                 temp_wait = 1
        # 			elif(vibration > 3.0 and earthquake_detect):
        # 				ser.write("2")
        # 				flag = 1
        #                 vibration_wait = 1
        # 			elif(gas >= 250.0 and gas_detect):
        # 				ser.write("3")
        # 				flag = 1
        #                 gas_wait = 1
        # 			if (flag == 0):
        # 				ser.write("0")
        # 			flag = 0
        # 			with open("./hazard.txt","a+") as output:
        # 				output.write(str1+"\n")
        # 			line = []
        # 			break
        # ser.close()
        print fire_detect, earthquake_detect, gas_detect
        time.sleep(3)

@app.route('/Settings', methods=['POST'])
def set_param():
    global fire_detect
    global gas_detect
    global earthquake_detect
    if(request.form.get('fire','')):
        fire_detect = 1
    else:
        fire_detect = 0
    if(request.form.get('gas','')):
        gas_detect = 1
    else:
        gas_detect = 0
    if(request.form.get('earthquake','')):
        earthquake_detect = 1
    else:
        earthquake_detect = 0
    print "updated values : "
    print fire_detect,earthquake_detect,gas_detect
    print "param updated!"
    return 'update successful'
# return app.send_static_file('Settings.html')
# return render(request, 'Settings.html',{'error_message': 'valid login', 'students': students, 'caretaker': caretaker, 'hostel': hostel})

@app.route('/')
def hello_world():
    return "Hello World!"

if __name__ == '__main__':
    global fire_detect
    global gas_detect
    global earthquake_detect
    t = threading.Thread(target=func, args=())
    t.start()
    app.run(host='127.0.0.1', port=8000, debug=True)

