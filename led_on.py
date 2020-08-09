#Simple example Robot Raconteur client light up M1K led
from RobotRaconteur.Client import *
import traceback
from js import print_div
####################Start Service and robot setup
async def led():
	try:
		m1k_obj=await RRN.AsyncConnectService('rr+ws://localhost:11111/?service=m1k',None,None,None,None)

		m1k_obj.async_setled(7,None)
	except:
		print_div(traceback.format_exc())

RR.WebLoop.run(led())
