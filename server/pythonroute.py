from bottle import route, get, post, run, template, static_file, request
import os
import json
import dbClient

@get('/mad/api/')
@get('/mad/api')
@get('/mad/api/')
@get('/mad/api/<path:path>')
def apiRoute(path=None):
    return static_file('views/soon.html' , root="")

@get('/mad/manager')
@get('/mad/manager/')
def managerRoute():
    return static_file('views/soon.html' , root="")

@get('/mad/')
@get('/')
@get('/mad')
def home():
    return static_file('views/home.html' , root="")

@get('/mad/postpage')
def test():
    return static_file('views/uploadimg.html' , root="")

@route('/mad/data', method='POST')
@route('/mad/post', method='POST')
def uploadFileToProject():
    projectid   = request.forms.get('projectid')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    db = dbClient.MAD_db()
    projectpath = db.getProjectPath(projectid)
    db.close()
    if ext in ('.png','.jpg','.jpeg', '.bmp', '.tif'):
        upload.save("projects/%s"%(projectpath)) # appends upload.filename automatically
    elif ext in ('.3gp','.m4a','.aac', '.aiff', '.flac', '.mp3', '.wav'):   
        upload.save("projects/%s"%(projectpath))
    elif ext in ('.stl','.obj','.fbx', '.dae', '.3ds', '.iges', '.step'):   
        upload.save("projects/%s"%(projectpath))
    else : 
        return 'File extension not allowed.'
    return 'Saved image named :' + upload.filename + 'in project :' + projectpath

@get('/mad/getdata')
def sendData():
    db = dbClient.MAD_db()
    res = None
    dataRequested = request.forms.get('request')
    if dataRequested == 'projects' : 
        res = db.getProjects()

    db.close()
    return res
        
with open('../config.json') as json_file:
    data = json.load(json_file)
    server_port = data[0]['bottle-server-port']

run(host='0.0.0.0', port=server_port)