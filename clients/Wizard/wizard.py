from tkinter import *
import pyautogui
import sys
from pathlib import Path

# As PosixPath
sys.path.append(str(Path(__file__).parent / ".."))
#sys.path.insert(0,"..") 
import MAD_client as mc
from datetime import datetime
import os, shutil
import copy
from tkinter import ttk 
import time
# class Screenshot(top) : 

class content_window :
	def __init__(self, top):
		self.photo= None #PhotoImage(file="images/rushhour.gif")
		self.header = Label(image = self.photo, bg="#FFF")
		self.body = None
		self.top = top
		self.header.pack()
		self.error = None
	def clear(self):
		if self.body:
			self.body.pack_forget()
			self.body = None
		if self.error:
			self.error.pack_forget()
			self.error = None

	def update(self,content):
		self.clear()
		self.body = content
		
	def show_error(self, string):
		if self.error:
			self.error.pack_forget()
		self.error = Label(text=string, bg="#F55", fg="#fff", font=("courier",20))
		self.error.pack(side=TOP)

	def close(self):
		self.top.destroy()

class Main_menu:
	def __init__(self, cw, project):
		self.top = cw
		self.content = Frame(bg="#fff")
		self.content.pack()
		self.screenshot = None
		self.project = project
		print("project:", self.project)
		Menubutton (self.content, text= "TAKE SCREENSHOT", command = lambda :self.takeScreenshot()).pack()
		Menubutton (self.content, text= "QUIT", command = lambda : self.top.close()).pack()
		self.top.update(self.content)
			
	def takeScreenshot(self): 
		self.top.top.attributes('-alpha', 0) #don't work weird
		if not os.path.exists('temp'):
			os.makedirs('temp')
		emptyDir('temp')
		now = datetime.now()
		self.screenshot = pyautogui.screenshot()
		filename = 'screenshot-%s.png'%(now.strftime("%m%d%Y%H%M%S"))
		path = 'temp/'+filename
		self.screenshot.save(path)
		time.sleep(1)
		self.top.top.attributes('-alpha', 1)
		connection.sendFileToProject(self.project['id'], path)
		emptyDir('temp')

class Login:
	def __init__(self, cw):
		self.top = cw
		self.content = Frame(bg="#fff")
		self.content.pack()
		self.project = None
		Label( self.content, textvariable= "Choose your project", relief=RAISED ).pack()

		projects = connection.getProjects()
		n = StringVar() 
		n.set("select your project")
		n.trace('w', self.cbcallback)
		cb  = ttk.Combobox(self.content, width = 27, textvariable = n)

		cb['values'] = [i['name'] for i in projects]
		cb.pack()

		Menubutton (self.content, text= "CONNECT", command = lambda : self.login(projects[cb.current()])).pack()
		Menubutton (self.content, text= "QUIT", command = lambda : self.top.close()).pack()
		self.top.update(self.content)

	def login(self, project):
		self.project = copy.deepcopy(project)
		print("logged to " + str(self.project['name']))
		fenetre.title("MAD wizard - %s"%(str(self.project['name'])))
		Main_menu(self.top, self.project)

	def cbcallback(self, *args):
		print("value changed")

class Menubutton(Button):
	def __init__(self, *args, **kwargs):
		Button.__init__(self,	
						height=2,
						fg = "#333",
						activeforeground = "#F55",
						bg = "#fff",
						activebackground="#fff",
						font =("Courier", 20),
						relief = FLAT,
						overrelief = FLAT,
						highlightthickness=0,
						borderwidth=0,
						*args, 
						**kwargs)


print("welcome to the wizard");

connection = mc.MAD_client()

def emptyDir(folder):
	for filename in os.listdir(folder):
			file_path = os.path.join(folder, filename)
			try:
					if os.path.isfile(file_path) or os.path.islink(file_path):
							os.unlink(file_path)
					elif os.path.isdir(file_path):
							shutil.rmtree(file_path)
			except Exception as e:
					print('Failed to delete %s. Reason: %s' % (file_path, e))

fenetre = Tk()
fenetre.geometry("300x400")
fenetre.configure(background="#fff")
fenetre.title("MAD wizard")
content = content_window(fenetre)
app = Login(content)
fenetre.mainloop()