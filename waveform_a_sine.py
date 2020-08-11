from RobotRaconteur.Client import *
import traceback
from js import print_div, document
####################Start Service and robot setup
ip=document.getElementById("ip").value
async def change_mode():
	try:
		m1k_obj=await RRN.AsyncConnectService('rr+ws://'+ip+':11111/?service=m1k',None,None,None,None)

		#set mode for each channel
		m1k_obj.async_setmode('A','SVMI',None)

		#get parameters
		min_value=float(document.getElementById("min").value)
		max_value=float(document.getElementById("max").value)
		frequency_value=float(document.getElementById("frequency").value)
		period_value=int(100000/frequency_value)
		delay=float(document.getElementById("delay").value)
		duty=float(document.getElementById("duty").value)

		#start waveform
		m1k_obj.async_wave('A', 'sine', min_value, max_value, period_value, -(period_value*delay), duty, None)
	except:
		print_div(traceback.format_exc())
	

RR.WebLoop.run(change_mode())
