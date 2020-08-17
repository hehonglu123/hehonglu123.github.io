from RobotRaconteur.Client import *
import traceback
from js import print_div, document, raise_err
####################Start Service and robot setup

async def change_mode():
	try:
		#get parameters
		min_value=float(document.getElementById("min").value)
		max_value=float(document.getElementById("max").value)
		frequency_value=float(document.getElementById("frequency").value)
		period_value=int(100000/frequency_value)
		delay=float(document.getElementById("delay").value)
		duty=float(document.getElementById("duty").value)
		if min_value>=max_value:
			raise_err("min>=max")
			return
		if delay>=1:
			raise_err("delay fraction>1")
			return
		if duty>=1:
			raise_err("duty cycle>1")
			return


		ip=document.getElementById("ip").value
		m1k_obj=await RRN.AsyncConnectService('rr+ws://'+ip+':11111/?service=m1k',None,None,None,None)

		#set mode for each channel
		m1k_obj.async_setmode('B','SVMI',None)

		#start waveform
		m1k_obj.async_wave('B', 'square', min_value, max_value, period_value, -(period_value*delay), duty, None)
	except:
		raise_err(traceback.format_exc())
	

RR.WebLoop.run(change_mode())
