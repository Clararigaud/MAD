#!/usr/bin/env python

# TODO : PROBLEM AFTER CALLING RECV() WEBSOCKETS DISCONNECTS... don't know > moving to js 
import sys
import websockets
# import RPi.GPIO as GPIO
import time
import requests
import asyncio
import json
class Unit(object):
	def __init__(self, name, unittype):
		self.name = name
		self.type = unittype
		self.address = 
		self.streamsource = None
		print("Hey, I'm %s, I'm a %s"%(self.name, self.type))
		#rospy.Subscriber('/toallunits', String, self.on_master_msg)
		
		#self.infopub = rospy.Publisher("/unit_info",unit_info, queue_size=10)
		
		# self.infosmsg = unit_info()
		# self.infosmsg.unit_name = self.name
		# # self.infosmsg.unit_type = self.type
		# self.hellopub = rospy.Publisher("/unit_log",unit_info, queue_size=10)
		# self.goodbyepub = rospy.Publisher("/unit_unlog",unit_info, queue_size=10)
		
		# Unit services 
		#client_connect = rospy.Service(rospy.get_name()+"/show_yourself", Trigger, self.show_myself)
		# while(self.hellopub.get_num_connections() == 0 and not rospy.is_shutdown()): 
		# 	rospy.loginfo("waiting for my master")
		# 	rospy.sleep(1)
		#self.hellopub.publish(self.infosmsg)
		#rospy.on_shutdown(self.sayGoodBye)

		
	async def run(self, websocket):
		async for message in websocket:
			event = json.loads(message)
			if event['type'] == "whoAreYou":
				print("received message from master")
				#self.master = websocket
				message_content = {'unit_name': self.name, 'unit_type': self.type}
				await webscoekts.send(json.dumps({'type': 'unit_log', 'message': message_content}))
			else:
				print(event)

	async def start(self):
		print ('Websocket NOT connected. Trying to reconnect.')
		self.ws = await websockets.connect("ws://localhost:8001/")
		# msg = json.dumps({"event":"pusher:subscribe","data":{"channel":"order_book"}})
		# await ws.send(msg)
		#async with websockets.connect("ws://localhost:8001/", ping_interval=None) as websocket:
		#await websocket.send("hello")
		while True:
			if not self.ws.open :
				self.ws = await websockets.connect("ws://localhost:8001/")
			print(self.ws.open)
			message = await self.ws.recv()
			event = json.loads(message)
			print(event)

			if not self.ws.open :
				self.ws = await websockets.connect("ws://localhost:8001/")			
			if event['type'] == "whoAreYou":
				print("received message from master")
				message_content = {'unit_name': self.name, 'unit_type': self.type}
				await self.ws.send(json.dumps({'type': 'unit_log', 'message': message_content}))
			else:
				print(event['type'])

	def on_master_msg(self, message):
		if(str(message.data)=="whosthere"):
			self.infopub.publish(self.infosmsg)
		print("new message from global")
		print(type(message.data))

	def show_myself(self,req):
		return {'success': True, 'message': ""}

	def sayGoodBye(self):
		self.goodbyepub.publish(self.infosmsg)


# class Clamp(Unit):
# 	def __init__(self,name, unittype):
# 		super(Clamp, self).__init__(name, unittype)
# 		# Param GPIOS adresses here

# 	def show_myself(self, req):
# 		# do the led job  
# 		return super(Clamp,self).show_myself(req)

# class Bot(Unit):
# 	def __init__(self,name, unittype):
# 		super(Bot, self).__init__(name, unittype)
# 		# Param GPIOS adresses here
# 		self.BUZ = 4

# 		#leds controls
# 		self.ledpub = rospy.Publisher(self.name+"/rgb_leds",RGB_LED, queue_size=10)

# 	def show_myself(self, req):
# 		#do the led job
# 		ledmsgoff = RGB_LED()
# 		ledmsgoff.function ='setLED'
# 		ledmsgoff.color = '000000'
# 		ledmsgoff.led1_color= '000000'
# 		ledmsgoff.led2_color= '000000'
# 		ledmsgoff.led3_color= '000000'
# 		ledmsgoff.led4_color= '000000'
# 		ledmsgoff.delay = 50
		

# 		ledmsgblink = RGB_LED()
#                 ledmsgblink.function ='rainbow'
#                 ledmsgblink.color = ''
#                 ledmsgblink.led1_color= ''
#                 ledmsgblink.led2_color= ''
#                 ledmsgblink.led3_color= ''
#                 ledmsgblink.led4_color= ''
#                 ledmsgblink.delay = 50

	
# 		self.ledpub.publish(ledmsgblink)
# 		GPIO.setmode(GPIO.BCM)
# 		GPIO.setwarnings(False)
# 		GPIO.setup(self.BUZ,GPIO.OUT)
# 		GPIO.output(self.BUZ,GPIO.HIGH)
# 		time.sleep(0.2)
# 		GPIO.output(self.BUZ,GPIO.LOW)

# 		time.sleep(2)
# 		self.ledpub.publish(ledmsgoff)
# 		return super(Bot, self).show_myself(req)

#async def main():

	#Cases unit type
unit_name = "Johnny"	
client = Unit(unit_name, None)  # No hanlde execution ? how 

# async with websockets.connect("ws://localhost:8001/"):
# 	print("Websocket client listening")
	#await asyncio.Future()  # run forever
asyncio.get_event_loop().run_until_complete(client.start())
#asyncio.run(client.run())
		#await recv()
