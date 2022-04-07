import os
import dbClient
from datetime import datetime

class SuDoc():
	def __init__(self):
		print("Controller initialized")
		self.projectRepo = "projects"

	def addEntry(self, project_id, time_start, time_end, file, entry_path=None):
		if(not entry_path):
			entry_path = 'entry_%i'%(int(self.getProject(project_id)['entries_count'])+1)
		name, ext = os.path.splitext(file.filename)
		# Add entry to Db
		db = dbClient.MAD_db()
		projectpath = db.getProjectPath(project_id)

		entry_id = db.createEntry(time_start, time_end, entry_path, project_id)
		# TODO later handle tags 
		db.close()
		now = datetime.now()
		self.setProject(project_id, "dateupdated", now.strftime("%m/%d/%Y, %H:%M:%S"))
		os.makedirs('%s/%s/%s'%(self.projectRepo, projectpath, entry_path))
		file.save("%s/%s/%s"%(self.projectRepo, projectpath, entry_path)) 

	def createProject(self):
		pass

	def setProject(self, project_id, field, value):
		db = dbClient.MAD_db()
		res = db.setProject(project_id, field, value)
		db.close()

	def getProjects(self, user_id= None):
		res = None
		db = dbClient.MAD_db()
		res = db.getProjects(user_id=user_id)
		db.close()
		return res

	def getProject(self, project_id, entries = False):
		res = None
		# get also entries and files
		db = dbClient.MAD_db()
		res = db.getProject(project_id, entries = entries)
		if(entries):

			for entry in res['entries']:
				entryFiles = os.listdir(self.projectRepo+'/'+ res['repo'] + '/' + entry['entry_path'])
				entry['files'] = []
				for filename in entryFiles:
					name, ext = os.path.splitext(filename)
					file = {}
					if ext in ('.png','.jpg','.jpeg', '.gif', '.bmp', '.tif'):
						file['type'] = 'bitmap'
					elif ext in ('.svg'):
						file['type'] = 'vector'
					elif ext in ('.mp4','.mov','.wmv','.avi','.avchd','.flv','.f4v','.swf','.mkv','.webm','.html5','.mpg','.mpeg','.m4v','.3gp','.3g2'):
						file['type'] = 'video'
					elif ext in ('.m4a','.aac', '.aiff', '.flac', '.mp3', '.wav'):   
						file['type'] = 'audio'
					elif ext in ('.stl','.obj','.fbx', '.dae', '.3ds', '.iges', '.step'):   
						file['type'] = '3Dfile'
					elif ext in ('.gcode'):
						file['type'] = 'gcode'
					else : 
						file['type'] = 'other'
					
					file['path'] = "/%s/%s/%s"%(res['repo'], entry['entry_path'], filename)
					file['name'] = filename
					file['extension'] = ext
					entry['files'].append(file)
		db.close()
		return dict(res)

	def getUser(self, userid):
		db = dbClient.MAD_db()
		res = db.getUser(userid)
		db.close()
		return res

	def getEntry(self, entry_id):
		pass

	def getRepoUrl(self):
		return self.projectRepo

if __name__ == '__main__':
	sudoc = SuDoc()
