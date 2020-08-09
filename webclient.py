from js import print_div
from js import document
from js import ImageData
from RobotRaconteur.Client import *
from matplotlib import pyplot as plt
import numpy as np
import time, traceback

periodvalue=100
x = np.linspace(0, 2, periodvalue)
y = np.zeros(periodvalue)

async def client_matplotlib():

	try:
		m1k_obj=await RRN.AsyncConnectService('rr+ws://localhost:11111/?service=m1k',None,None,None,None)
		#set mode for each channel
		m1k_obj.async_setmode('A','SVMI',None)
		m1k_obj.async_setmode('B','HI_Z',None)
		#start waveform
		m1k_obj.async_wave('A', 'triangle', 0, 5, periodvalue, -(periodvalue / 4), 0.5, None)

		#start streaming
		m1k_obj.async_StartStreaming(None)
		
		print_div("Running!")
		#plot
		fig, ax = plt.subplots()
		fig.show()	

		while True:
			try:
				await animate(0,m1k_obj,ax)
			except RR.ValueNotSet:
				pass

	except:
		print_div(traceback.format_exc())
		m1k_obj.async_StopStreaming(None)
		raise

async def animate(i, m1k_obj,ax):
	global x, y
	sample=await m1k_obj.samples.AsyncPeekInValue(None)
	y=np.roll(y,1)
	y[0]=sample[0].B[0]
	# Draw x and y lists
	ax.clear()
	ax.plot(x, y,'ro')

	#text display
	props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
	text_m1k = '\n'.join((
	r'$ChA:V=%.2f$' % (sample[0].A[0], ),
	r'$ChA:I=%.2f$' % (sample[0].A[1], ),
	r'$ChB:V=%.2f$' % (sample[0].B[0], ),
	r'$ChB:I=%.2f$' % (sample[0].B[1], )))

	ax.text(0.75, 0.95, text_m1k, transform=ax.transAxes, fontsize=14,
			verticalalignment='top', bbox=props)


RR.WebLoop.run(client_matplotlib())