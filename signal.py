import serial
import time

# Import package
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Define Variables
MQTT_BROKER = "192.168.1.101"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "Hazard"
MQTT_TOPIC_FIRE = "fire_active"
MQTT_TOPIC_GAS = "gas_active"
MQTT_TOPIC_EARTHQUAKE = "earthquake_active"

TOPICS = ["Gas", "Temperature", "Vibration"]

ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)

# Define on_connect event Handler
def on_connect(mosq, obj, rc):
	#Subscribe to a the Topic
	mqttc.subscribe(MQTT_TOPIC, 0)
	mqttc.subscribe(MQTT_TOPIC_FIRE, 0)
	mqttc.subscribe(MQTT_TOPIC_GAS, 0)
	mqttc.subscribe(MQTT_TOPIC_EARTHQUAKE, 0)
	print "Subscribing..."

# Define on_subscribe event Handler
def on_subscribe(mosq, obj, mid, granted_qos):
    print "Subscribed to MQTT Topic"

# Define on_message event Handler
def on_message(mosq, obj, msg):
	if (msg.topic == "fire_active"):
		print msg.payload
		if (msg.payload == "on"):
			fire_active = 1
			print "fire alarm enabled"
		elif (msg.payload == "off"):
			fire_active = 0
			print "fire alarm disabled"
	elif (msg.topic == "gas_active"):
		print msg
		if (msg.payload == "on"):
			gas_active = 1
			print "gas alarm  enabled"
		elif (msg.payload == "off"):
			gas_active = 0
			print "gas alarm disabled"
	elif (msg.topic == "earthquake_active"):
		print msg
		if (msg.payload == "on"):
			earthquake_active = 1
			print "earthquake alarm enabled"
		elif (msg.payload == "off"):
			earthquake_active = 0
			print "earthuake alaem disabled"
	else:
		print msg.payload

#	print msg.payload

def get_msgs(values):
	msgs = [];
	for key in values:
		msgs.append({'topic': key, 'payload': values[key]});
	return msgs;

# Initiate MQTT Client
mqttc = mqtt.Client()

# Register Event Handlers
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect with MQTT Broker
mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL )

mqttc.loop_start()

temp_wait = 0
gas_wait = 0
vibration_wait = 0
fire_active = 1
gas_active = 1
earthquake_active  = 1
vibration = 0
temp_last_non_zero = 0
#this will store the line
line = []
values = {}
flag = 0
ser.write("0")
start = time.time()
last = time.time()
temperature = 0
while True:
	
	if(temp_wait or vibration_wait or gas_wait):
		if(time.time()-start>=0.5):
			temp_wait = 0
			vibration_wait = 0
			gas_wait = 0

	'''#setting user preference by use of web interface
	file = open("userpref.txt", "r")
	pref = file.readline()
	if len(pref) > 0 : 
		sett = pref.split()
		if(sett[0] == '0'):
			fire_active = 0 
		else: 
			fire_active  = 1
		if(sett[1] == '0'):
			earthquake_active = 0
		else:
			earthquake_active = 1
		if(sett[2] == '0'):
			gas_active = 0
		else:
			gas_active = 1
	file.close()
	'''
	#reading serial port input (sensor data) received by xbee from remote xbee
	#reading till it is available
	while ser.inWaiting():
		for c in ser.read():
			line.append(c)
			if c == '\n':
				str1=''.join(line)
				print("(Temp,Vibration,Gas) : " + str1)
				line = str1.split()
				temperature = float(line[0])
				vibration = float(line[1])
				gas = float(line[2])
				if(temperature > 0):
					temp_last_non_zero = temperature
				#data to publish

				values['Temperature']=temp_last_non_zero
				values['Gas']=gas
				values['Vibration']=vibration

				#temp reading to send to plot.il live graph api
				with open("./temp_reading.txt", "w+") as output:
					output.write(str(temperature))

				#sending response to remote xbee/arduino
				if(temp_wait or vibration_wait or gas_wait):
					ser.write("0")
					print "0 sent"
				else:
					if(temperature >= 28.0 and fire_active == 1):
						#ring buzzer for fire
						ser.write("1")
						print "1 sent"
						flag = 1
						start = time.time()
						temp_wait = 1
					elif(vibration > 3.0 and earthquake_active == 1):
						#ring buzzerr for earthquake
						print "Vibration threshold"
						ser.write("2")
						print "2 sent"
						start = time.time()
						flag = 1
						vibration_wait = 1
					elif(gas <= 3.90 and gas_active == 1):
						#ring buzzer for gas leakage
						ser.write("3")
						print "3 sent"
						flag = 1
						start = time.time()
						gas_wait = 1
					if (flag == 0 ):
						ser.write("0")
						print "0 sent"
					flag = 0
				with open("./hazard.txt","a+") as output:
					output.write(str1+"\n")
				line = []
				break

	#sending the last input to mqtt broker
	if(time.time()-last>2.0 or vibration >= 3.0):
		last = time.time()
		msgs = get_msgs(values);
		#print msgs
		if (len(msgs)>0): 
			publish.multiple(msgs, hostname=MQTT_BROKER, port=MQTT_PORT, keepalive=MQTT_KEEPALIVE_INTERVAL);
	
mqttc.loop_stop()
mqtt.disconnect()	
ser.close()
