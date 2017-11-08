import serial
import time
import plotly
import plotly.tools as tls
from plotly.graph_objs import *
import datetime
import time
import numpy as np
import json
import plotly.plotly as py
import plotly.graph_objs as go
import random 


# (@) Make instance of the Stream link object, 
#     with same stream id as Stream id object
stream_ids = tls.get_credentials_file()['stream_ids']
stream_id = stream_ids[0]
stream = Stream(
	token=stream_id,
	maxpoints=80
)
trace1 = Scatter(
	x=[],
	y=[],
	mode='lines+markers',
	stream=stream
)
data=Data([trace1])
layout = Layout(title='Time Series')
fig = Figure(data=data, layout=layout)
unique_url = py.plot(fig, filename='meet_first_stream')
s = py.Stream(stream_id)

# (@) Open the stream
s.open()

# (*) Import module keep track and format current time
import datetime
import time

i = 0    # a counter
k = 5    # some shape parameter
N = 50000  # number of points to be plotted

# Delay start of stream by 5 sec (time to switch tabs)
time.sleep(5)

#this will store the line
line = []
temperature= 0
gas = 0
vibration = 0

while i<N:
	file = open("temp_reading.txt", "r")
	pref = file.readline()
	if len(pref) > 0: 
		sett = pref.split()
		print "sett[0] :" , sett[0]
		if(float(sett[0]) > 0):
			temperature = float(sett[0])
			#send data			
			i=i+1
			# Current time on x-axis, temperature on y-axis
			x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
			y = temperature
   			# (-) Both x and y are numbers (i.e. not lists nor arrays)
    		# (@) write to Plotly stream!
			s.write(dict(x=x, y=y))
	    	# (!) Write numbers to stream to append current data on plot,
    		#     write lists to overwrite existing data on plot (more in 7.2).

			time.sleep(0.5)  # (!) plot a point every 500 ms, for smoother plotting

s.close()

ser.close()
