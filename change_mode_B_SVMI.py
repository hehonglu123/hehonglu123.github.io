from RobotRaconteur.Client import *
import traceback
from js import print_div
####################Start Service and robot setup
ip='128.213.64.202'
async def change_mode():
	m1k_obj=await RRN.AsyncConnectService('rr+ws://'+ip+'/?service=m1k',None,None,None,None)

	#set mode for each channel
	m1k_obj.async_setmode('B','SVMI',None)

RR.WebLoop.run(change_mode())
