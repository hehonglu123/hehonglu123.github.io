from js import print_div, document, raise_err
from RobotRaconteur.Client import *
import numpy as np
import time, traceback
from js import Plotly

# globals
SAMPLE_RATE=100000
timestamp=None
time_axis=None

async def client_plotly():
	global m1k_obj,time_axis,x,y_A,y_B
	try:
		#IP of service
		ip=document.getElementById("ip").value
		# set log level for debug
		# RRN.SetLogLevel(RR.LogLevel_Debug)
		#connect to service
		sub=RRN.SubscribeService('rr+ws://'+ip+':11111/?service=m1k')
		while True:
			try:	
				m1k_obj = sub.GetDefaultClient()
				break
			except RR.ConnectionException:
				await RRN.AsyncSleep(1, None)
		# m1k_obj = sub.AsyncGetDefaultClient(30)

		#subscribe to wire
		samples_wire=sub.SubscribeWire("samples")

		#reset mode for each channel
		# m1k_obj.async_setmode('A','HI_Z',None)
		# m1k_obj.async_setmode('B','HI_Z',None)

		

		#start streaming
		await m1k_obj.async_set_sample_size(100,None)
		try:
			m1k_obj.async_StartStreaming(None)
		except:
			pass

		#hide start button
		document.getElementById("start").style.display = "none";


		while True:
			try:
				
				time_axis_new=int(document.getElementById("slide").value)
				if time_axis_new!=time_axis:	
					time_axis=int(document.getElementById("slide").value)	
					frequency=int(document.getElementById("frequency").value)

					cycles_onscreen=time_axis/(1000/frequency)
					if cycles_onscreen<1:
						raise_err("time axis must be greater than 1000/freq")

					#plot settings
					points_onscreen=int(time_axis*SAMPLE_RATE/1000)		#ensure time_axis is accurate, based on sampling rate
					
					await m1k_obj.async_set_sample_size(int(points_onscreen/cycles_onscreen),None)
					# await m1k_obj.async_set_sample_size(1000,None)
					x = np.linspace(0, time_axis, points_onscreen)
					y_A = np.zeros(points_onscreen)
					y_B = np.zeros(points_onscreen)

				time_axis=time_axis_new

				#leave time for background
				await RRN.AsyncSleep(0.001, None)
				await plot(samples_wire)

				
			except RR.RobotRaconteurPythonError.ValueNotSetException:
				pass

	except:
		raise_err(traceback.format_exc())
		m1k_obj.async_StopStreaming(None)
		raise

async def plot(samples_wire):
	global x, y_A, y_B, timestamp, m1k_obj

	#check if new data received
	sample_packet=samples_wire.TryGetInValue()
	if (not sample_packet[0]) or sample_packet[-1]==timestamp:
		return 

	samples=sample_packet[1]
	timestamp=sample_packet[-1]	

	stream_num_sample=await m1k_obj.async_get_sample_size(None)

	try:
		y_A=np.roll(y_A,stream_num_sample)
		y_A[:stream_num_sample]=samples[::4]
		y_B=np.roll(y_B,stream_num_sample)
		y_B[:stream_num_sample]=samples[2::4]
	except ValueError:
		pass


	waveform_A={ 'y': y_A, 'x': x ,'xaxis': 'x2', 'yaxis': 'y2' ,'mode':'lines','name':'channel_A','type':'scatter','marker':{'size':10,'color':'#e31010'}}
	waveform_B={ 'y': y_B, 'x': x ,'xaxis': 'x1', 'yaxis': 'y1' ,'mode':'lines','name':'channel_B','type':'scatter','marker':{'size':10,'color':'#0000FF'}}

	layout = {
	'grid': {
	'rows': 2,
	'columns': 1,
	'pattern': 'independent',
	'roworder': 'bottom to top'
	},
	'xaxis': {
	'autorange': True
	},
	'yaxis1': {
	'range': [0, 5],
	'autorange': False
	},
	'yaxis2': {
	'range': [0, 5],
	'autorange': False
	},
	'annotations': [
	{
	'xref': 'paper',
	'yref': 'paper',
	'x': 0,
	'xanchor': 'right',
	'y': 1,
	'yanchor': 'bottom',
	'text': 'Voltage (V)',
	'showarrow': False
	}, {
	'xref': 'paper',
	'yref': 'paper',
	'x': 1,
	'xanchor': 'left',
	'y': 0,
	'yanchor': 'top',
	'text': '  ms',
	'showarrow': False}
	]
	}
	Plotly.react('plot',[waveform_A, waveform_B],layout)


RR.WebLoop.run(client_plotly())