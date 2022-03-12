import sqlite3
from datetime import datetime

class MAD_db():
	def __init__(self):
		self.conn = sqlite3.connect('mom.db')
		self.c = self.conn.cursor()
		print("dbConnector initialized")

	def close(self):
		self.conn.close()

	def createProject(self, project_name, project_userIds, project_type, project_url = None): #repo type : ( we souhld ultimately be able to access git style repos)
		project_repo = "project_name" # then create git rpos
		project_state = 1 #state=1 for "en cours"
		now = datetime.now()
		req = 'INSERT INTO projets(name,datecreated, dateupdated, repo, projecturl, type, state) VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(project_name, now.strftime("%m/%d/%Y, %H:%M:%S"),now.strftime("%m/%d/%Y, %H:%M:%S"), project_repo, project_url, project_type, project_state)
		self.c.execute(req)
		print("created new project :" + project_name)

		project_id = self.c.lastrowid

		for user_id in project_userIds :
			self.c.execute("INSERT INTO usersprojects(userid,projectid) VALUES(%s,%s)"%(user_id, project_id))
			print("Added new user :" + self.getUserNameById(user_id))

		self.conn.commit()
		return project_id

	def createEntry(self, time_start, time_end, entry_path, project_id):
		req = 'INSERT INTO entries(time_start, time_end, entry_path, project_id) VALUES(\'%s\',\'%s\',\'%s\',\'%s\')'%(time_start, time_end, entry_path, project_id)		
		self.c.execute(req)
		print("created new entry at :" + entry_path)
		entry_id = self.c.lastrowid
		self.conn.commit()
		return entry_id

	def editEntry():
		pass

	def getProjectRepo(self):
		pass

	def getUsers(self):
		pass

	def getProjects(self, user_id=None):

		if user_id:
			self.c.execute('SELECT * FROM projets INNER JOIN usersprojects ON projets.id = usersprojects.projectid WHERE userid = %s'%(user_id))
		else :
			self.c.execute('SELECT * FROM projets')

		field_names = [i[0] for i in self.c.description]
		res = self.c.fetchall()
		resTab = []
		for p in res :
			resTab.append(dict(self.getNiceProjectFields(p, field_names)))
		return resTab

	def getNiceProjectFields(self, row, field_names):
		resDict = {}
		for i, col in enumerate(field_names) :
			resDict[col] = row[i]
		p_id  = resDict['id']
		self.c.execute('SELECT utilisateurs.nom, utilisateurs.prenom, utilisateurs.id FROM utilisateurs INNER JOIN usersprojects ON utilisateurs.id = usersprojects.userid WHERE projectid = %s'%(p_id))
		users = [{'lastname' : u[0], 'firstname':u[1], 'id' : u[2]} for u in self.c.fetchall()]
		resDict['users'] = users
		return resDict

	def getProject(self, p_id, entries=False):
		self.c.execute('SELECT * FROM projets WHERE id = %s'%(p_id))
		field_names = [i[0] for i in self.c.description]
		res = self.c.fetchone()
		resDict = self.getNiceProjectFields(res, field_names)
		resentries = self.getProjectEntries(p_id)
		resDict['entries_count'] = len(resentries)
		if(entries):
			resDict['entries'] = resentries
		return dict(resDict)

	def getProjectEntries(self, p_id):
		self.c.execute('SELECT * FROM entries WHERE project_id = %s'%(p_id))
		field_names = [i[0] for i in self.c.description]
		res = self.c.fetchall()
		resTab = []
		for p in res :
			resDict = {}
			for i, col in enumerate(field_names) :
				resDict[col] = p[i]
			resTab.append(resDict)
		return resTab

	def setProject(self, project_id, field, value):
		self.c.execute('UPDATE projets SET %s = \'%s\' WHERE id= %s'%(field, value, project_id))


	def getProjectPath(self, p_id):
		self.c.execute('SELECT repo FROM projets WHERE id = %s'%(p_id))
		res = self.c.fetchone()
		return str(res[0])

	def getUserNameById(self, user_id):
		self.c.execute('SELECT nom FROM utilisateurs WHERE id = %s'%(user_id))
		res = self.c.fetchone()
		print(type(res))
		return str(res[0])

	def getProjectNameById(self, id):
		pass
