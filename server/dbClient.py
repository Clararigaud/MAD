import sqlite3
from datetime import datetime
import json

class MAD_db():
	def __init__(self):
		self.conn = sqlite3.connect('mom.db')
		self.c = self.conn.cursor()
		print("dbConnector initialized")

	def close(self):
		self.conn.close()

	def createProject(self, project_name, project_userIds, project_repo = None ): #repo type : ( we souhld ultimately be able to access git style repos)
		now = datetime.now()
		req = 'INSERT INTO projects(name,datecreated,repo) VALUES(\'%s\',\'%s\',\'%s\')'%(project_name, now.strftime("%m/%d/%Y, %H:%M:%S"), project_repo)

		print(req)
		self.c.execute(req)
		print("created new project :" + project_name)

		project_id = self.c.lastrowid

		for user_id in project_userIds :
			self.c.execute("INSERT INTO usersprojects(userid,projectid) VALUES(%s,%s)"%(user_id, project_id))
			print("Added new user :" + self.getUserNameById(user_id))

		self.conn.commit()
		return project_id

	def getProjectRepo(self):
		pass

	def getUsers(self):
		pass

	def getProjects(self):
		self.c.execute('SELECT * FROM projects')
		field_names = [i[0] for i in self.c.description]
		res = self.c.fetchall()
		resDict = []
		for p in res :
			resDict.append({})
			for i, col in enumerate(field_names) :
				resDict[-1][col] = p[i]
			p_id  = resDict[-1]['id']
			self.c.execute('SELECT users.firstname, users.id FROM users INNER JOIN usersprojects ON users.id = usersprojects.userid WHERE projectid = %s'%(p_id))
			users = [{'name' : u[0], 'id' : u[1]} for u in self.c.fetchall()]
			resDict[-1]['users'] = users

		return json.dumps(resDict)
		
	def getProjectPath(self, p_id):
		self.c.execute('SELECT repo FROM projects WHERE id = %s'%(p_id))
		res = self.c.fetchone()
		return str(res[0])

	def getUserNameById(self, user_id):
		self.c.execute('SELECT firstname FROM users WHERE id = %s'%(user_id))
		res = self.c.fetchone()
		print(type(res))
		return str(res[0])


	def postFileToProject(self, project_id, file):
		pass
	def getProjectNameById(self, id):
		pass

		
# Create table
# c.execute('''CREATE TABLE stocks
#              (date text, trans text, symbol text, qty real, price real)''')

# # Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# # Save (commit) the changes
# conn.commit()
# for row in c.execute('SELECT * FROM users ORDER BY id'):
# 	print("row")
# 	print(row)
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
