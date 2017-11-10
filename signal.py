import serial
import time

# Import package
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Define Variables
MQTT_BROKER = "192.168.1.101"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
# Topic for sending sensor data
MQTT_TOPIC = "Hazard"

#Topics for receiving sensor's activation from user
MQTT_TOPIC_FIRE = "fire_active"	
MQTT_TOPIC_GAS = "gas_active"
MQTT_TOPIC_EARTHQUAKE = "earthquake_active"

#subtopics to send
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
	#Subscribe to all the Topic
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
			print "earthuake alarm disabled"
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

#this will store the line
line = []
values = {}
flag = 0
ser.write("0")
start = time.time()
last = time.time()
while True:
	
	if(temp_wait or vibration_wait or gas_wait):
		if(time.time()-start>=0.5):
			temp_wait = 0
			vibration_wait = 0
			gas_wait = 0

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

				#data to publish
				values['Temperature']=temperature
				values['Gas']=gas
				values['Vibration']=vibration

				#temp reading to send to plot.il live graph api
				with open("./temp_reading.txt", "w+") as output:
					output.write(str(temperature))

				#sending response to remote xbee/arduino
				if(temp_wait or vibration_wait or gas_wait):
					ser.write("0")
				else:
					if(temperature >= 27.0 and fire_active == 1):
						#ring buzzer for fire
						ser.write("1")
						flag = 1
						start = time.time()
						temp_wait = 1
					elif(vibration > 3.0 and earthquake_active == 1):
						#ring buzzerr for earthquake
						ser.write("2")
						start = time.time()
						flag = 1
						vibration_wait = 1
<<<<<<< HEAD
					elif(gas <= 0.4 and gas_active == 1):
=======
					elif(gas >= 250.0 and gas_active == 1):
>>>>>>> 6865bcf1c1ccf1019ef9e98c3012ec114a7f3ece
						#ring buzzer for gas leakage
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

	#sending the last input to mqtt broker at interval of 2 seconds.
	if(time.time()-last>2 and temperature > 0):
		last = time.time()
		msgs = get_msgs(values);
		print msgs
		if (len(msgs)>0): 
			publish.multiple(msgs, hostname=MQTT_BROKER, port=MQTT_PORT, keepalive=MQTT_KEEPALIVE_INTERVAL);
	
mqttc.loop_stop()
mqtt.disconnect()	
<<<<<<< HEAD
ser.close()
=======
ser.close()
>>>>>>> 6865bcf1c1ccf1019ef9e98c3012ec114a7f3ece
