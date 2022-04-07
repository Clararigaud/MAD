#import http.client
import json
import os,sys,inspect,shutil
import requests
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
class SuDoc_client:
	def __init__(self):
		with open(currentdir+'/../config.json') as json_file:
			data = json.load(json_file)
			self.server_port = data[0]['bottle-server-port']
			self.server_address = data[0]['bottle-server-address']
		#self.connection = http.client.HTTPConnection(server_address, server_port)
		#print("Connected to ", server_address)

	def sendFileToProject(self, project, file):
		# json_data = json.dumps({'file' : file, 'project' : project})
		# headers = {'Content-type': 'application/json'}
		#self.connection.request('POST', '/mad/post', json_data, headers)
		#r = requests.post(self.posturl, data = {'project': project} , files = {'upload_file' : open(file, 'rb')})
		r = requests.post('http://%s:%s/sudoc/postentry'%(self.server_address,str(self.server_port)), data = {'projectid':project}, files= {'files' : open(file, 'rb')})

	def getProjects(self):
		r = requests.get('http://%s:%s/sudoc/getprojects'%(self.server_address,str(self.server_port)), data = {'request':'projects'})
		return r.json()