#Simple example Robot Raconteur client light up M1K led
from RobotRaconteur.Client import *
import traceback
from js import print_div
####################Start Service and robot setup
ip='192.168.1.233'
async def led():
	try:
		m1k_obj=await RRN.AsyncConnectService('rr+ws://'+ip+'/?service=m1k',None,None,None,None)

		m1k_obj.async_setled(0,None)
	except:
		print_div(traceback.format_exc())

RR.WebLoop.run(led())
