# WEBSOCKETS server 
import asyncio
import websockets
import json
from datetime import datetime

import traceback
import logging
class Capush():
	def __init__(self):
		self.units = {}
		self.project_unit_connections = {}
		self.websocket_connections = [] # all websocket connections (to broadcast)
		self.units_websockets = {} # "websocket.id" : UnitName
		self.unitListTopic = 'unit_list'
		self.check_units()

	async def handler(self, websocket):
		print('handling websocket')
		try:
			if(websocket not in self.websocket_connections):
				websocket.id = len(self.websocket_connections) +1 
				self.websocket_connections.append(websocket)
			async for message in websocket:
				event = json.loads(message)
				if(type(event) == dict):
					if event['type'] == 'init':
						if("client_type" in event['message']):
							if(event['message']["client_type"] == 'manager'):
								print('First message from manager:')
								print(event['message'])
								await self.publish_units_status()
							elif(event['message']["client_type"] == 'unit'):
								print('First message from unit:' + event['message']['unit_name'])
								print(event['message'])
								self.units_websockets[websocket.id] = event['message']['unit_name']
								await self.on_new_unit(event['message'])

					elif event['type'] == 'unit_list_request':
						await self.publish_units_status()
					elif event['type'] == 'project_unit_connect_request':
						await self.on_webclient_connection_request(websocket, event['message'])
					elif event['type'] == 'project_unit_disconnect_request':
						await self.on_webclient_disconnection_request(websocket, event['message'])
					elif event['type'] == 'unit_info':
						await self.on_unit_info(event['message'])
					elif event['type'] == 'unit_log':
						await self.on_new_unit(event['message'])
					elif event['type'] == 'unit_unlog':
						await self.on_unit_dies(event['message'])
					else:
						print("event type is unknown")
						print(event)
				else:
					print('event is not a dict')
					print(event)

		except websockets.ConnectionClosed:
			print("connexion with %s has been lost, removing"%(self.units_websockets[websocket.id]))
			self.websocket_connections.remove(websocket)
			await self.on_unit_dies(self.units_websockets[websocket.id])

		except Exception as e:
			logging.error(traceback.format_exc())
		
	async def publish_units_status(self):
		self.check_units();
		res = {"all" : {}, "available":{}}
		for unit in self.units :
			res["all"][unit] = self.units[unit].asDict()
			if(self.units[unit].isAvalaible()):
				res["available"][unit] = self.units[unit].asDict()
		event = {
			'type': self.unitListTopic,
			"message": res
		}
		websockets.broadcast(self.websocket_connections, json.dumps(event))		

# 	def infos_log(self):
# 		rospy.loginfo("Controller status \n : %i unit connected"%(len(self.units)))
# 		jsonStr = json.JSONEncoder().encode([unit.asDict() for unit in self.units.values()])
# 		rospy.loginfo(jsonStr)
	
	async def on_new_unit(self, data):
		self.units[data['unit_name']] = Unit(data['unit_name'])
		print("New unit connected \n : %s "%(data['unit_name']))
		#self.infos_log()
		await self.publish_units_status()

	async def on_unit_dies(self, unit_name):
		print("Unit has died \n : %s "%(unit_name))
		await self.on_unit_lost(unit_name)
		await self.publish_units_status()

	def check_units(self): # check if the unit node is still active
		pass

	async def on_unit_lost(self, unitname):
		if(self.units[unitname].getStatus() == 2):
			await self.destroy_project_unit_connection(self.units[unitname].connectedto, unitname)
		del self.units[unitname]

	async def on_unit_info(self, data):
		print("Received update from %s "%(data.unit_name))

	async def on_webclient_connection_request(self, websocket, msg):
		print("Received request from client")
		unitname = msg["unit_name"]
		username = msg["project_name"]
		ansdict = {}
		ansdict["project_name"] = username
		ansdict["unit_name"] = unitname
		self.check_units()
		if(unitname in self.units):
			if(self.units[unitname].isAvalaible()):
					ansdict["accepted"] = 1
					ansdict["msg"] = "Your connection to %s has been confirmed"%(unitname)
					await self.create_project_unit_connection(username, unitname)
			else:
				#not available
				ansdict["accepted"] = 0
				ansdict["msg"] = "Connection refused, %s is not available"%(unitname)
		else:
			#No unit named
			ansdict["accepted"] = 0
			ansdict["msg"] = "Connection refused, no unit named %s"%(unitname)

		await self.publish_units_status()

		event = {
			"type": 'webclient_unit_connect_response',
			"message": ansdict
		}

		await websocket.send(json.dumps(event))

	async def create_project_unit_connection(self, username, unitname):
		if(username not in self.project_unit_connections):
			self.project_unit_connections[username] = {}
		self.units[unitname].startWebConnection(username)
		self.project_unit_connections[username][unitname] = web_unit_session(username, unitname);
		await self.publish_units_status()

	async def destroy_project_unit_connection(self,username, unitname):
		if (username in self.project_unit_connections):
			if(unitname in self.project_unit_connections[username]):
				del self.project_unit_connections[username][unitname]
		else :
			print("Session to be detroyed wasn't recorded... ")
		if unitname in self.units:
			self.units[unitname].endWebConnection()
		await self.publish_units_status()

	async def on_webclient_disconnection_request(self, websocket, msg):
		print("Received disconnection request from client")
		username = msg["project_name"]
		unitname = msg["unit_name"]

		ansdict = {}
		ansdict["project_name"] = username
		ansdict["unit_name"] = unitname

		await self.destroy_project_unit_connection(username, unitname)
		ansdict["accepted"] = 1
		ansdict["msg"] = "Connection to %s closed"%(unitname)
		ansdict["unitname"] = unitname
		event = {
			"type": 'webclient_unit_disconnect_response',
			"message": ansdict
		}

		await websocket.send(json.dumps(event))

	def getAllUnitsAsDict(self, available_only):
		res = {}
		for unit in self.units :
			if(self.units[unit].isAvalaible() or not available_only):
				res[unit] = self.units[unit].asDict()
		return res

class Unit():
	def __init__(self, namespace, bot_type = "base"):
		self.namespace = namespace
		self.bottype = bot_type
		self._status = 1
		self._last_status_update = datetime.now()
		self._location = ""
		self._last_location_update = datetime.now()
		self.connectedto = None

	def asDict(self):
		return {
		"name" : self.namespace, "type" : self.bottype, 
		"status" : self._status, 
		"location" : self._location, 
		"last_location_update" : self._last_location_update.strftime("%H:%M:%S"), 
		"last_status_update": self._last_status_update.strftime("%H:%M:%S")
		}
	def getStatus(self):
		return self._status

	def updateLocation(self, loc):
		self._location = loc
		self._last_location_update = datetime.now()

	def updateStatus(self, status): # led activity change 
		self._status = status
		self._last_status_update = datetime.now()

	def isAvalaible(self):
		return self._status == 1
	def startWebConnection(self, username):
		self.updateStatus(2)
		self.connectedto = username

	def endWebConnection(self):
		self.updateStatus(1)
		self.connectedto = None
	# def __del__(self):

class web_unit_session():
	def __init__(self, project_name, unit_name):
		self.username = project_name;
		self.unitname = unit_name;
		self.webclient_connectionstart = datetime.now()
		print("Connection from %s to %s started at %s"%(self.username, self.unitname, self.webclient_connectionstart.strftime("%H:%M:%S")))
	
	def log(self, tolog): # use to log session activity 
		print("Must log this into a file")

	def __del__(self):
		print("Connection from %s to %s ended at %s"%(self.username, self.unitname, datetime.now().strftime("%H:%M:%S")))

async def main():
	controller = Capush()
	async with websockets.serve(controller.handler, "", 8001):
		print("Websocket started")
		await asyncio.Future() # run forever

asyncio.run(main())