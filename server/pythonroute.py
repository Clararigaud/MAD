from bottle import route, get, post, run, template, static_file, request, error, view
import json
import controller
from datetime import datetime


@get('/sudoc')
@get('/sudoc/')
@get('/sudoc/projects')
@view("projects_page.tpl")  
def projects_page() :
    return {"projects":sudoc.getProjects(user_id = None)}

@get('/sudoc/project')
@view("project_page.tpl")  
def projectsRoute():
    projectid = request.params.id
    entries = True
    res = sudoc.getProject(projectid, entries = entries)
    return {"project":res}

@error(404)
def error404(error):
    return 'Nothing here, sorry'

@get('/sudoc/repository/<filepath:path>')
def sendRepositoryFile(filepath=None):
    # just sending back local files for now
    if(filepath) :
        return static_file(filepath , root=sudoc.getRepoUrl())
    else:
        return static_file('404.html' , root="views")

@get('/sudoc/css/<filepath:path>')
def sendCss(filepath):
    return static_file(filepath , root='views/css/')

#http requests handlers V V V
@post('/sudoc/postentry')
def uploadFileToProject():
    projectid   = request.forms.get('projectid')
    data     = request.files.get('files')
    now = datetime.now()
    time_start = now.strftime("%m/%d/%Y, %H:%M:%S")
    time_end = now.strftime("%m/%d/%Y, %H:%M:%S")
    res = sudoc.addEntry(projectid, time_start, time_end, data)
    return json.dumps(res)

@get('/sudoc/getprojects') #TODO add selectors / criteria : user, machine, tool, espace, state / lastupdated, last created / limnumber 
def sendProjects():
    user_id = request.forms.get('user_id')
    res = sudoc.getProjects(user_id = user_id)
    return json.dumps(res)

@get('/sudoc/getproject')
def sendProject():
    projectid = request.params.id
    entries = request.params.entries
    res = sudoc.getProject(projectid, entries = entries)
    return json.dumps(res)
        
with open('../config.json') as json_file:
    data = json.load(json_file)
    server_port = data[0]['bottle-server-port']
    sudoc = controller.SuDoc()

run(host='0.0.0.0', port=server_port)