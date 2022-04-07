# Sudoc 
This is the architecture client / server of our Affable project

## Current state of implementation

### Server 

A config file enable anybody to keep his own setup : see [config.json](config.json)

#### Http Server - Python Bottle - SQLLite
A Http server can be ran with the [main.py](server/main.py) script.

Once running, you can navigate with the url and ports specified in the **config.json** file like 
> your.local.ip.address:8081/sudoc

Currently there are things in : 
- **/sudoc** : The welcome to server page / displays all projects, by clicking on a project you can display the details and entries
<!-- - **/mad/api** : The future subdomain which will listen to requests for accessing realtime datas from influxdb, allow to automatically generate reports on a lab, a machine, a project.
- **/mad/manager** : The interface for managing projects (creating new, editing, adding users)
- **/mad/postpage** : to post a file to a project (only project ID based for now) -->

<!-- #### MQTT Server - InfluxDB
If you have an installation of MQTT and influxdb, you can run the script [main.py](server/main.py) which only takes care of listening MQTT messages and save them inside influxdb
 -->
### Http clients
[MAD_client.py](clients/MAD_client.py) script takes care of all functions which send requests to the server, if you want you client to interact with the server, you should consider to use the functions inside this class (if not implemented ask Clara to do it)

Currently there are this clients : 
- **[Wizard](clients/Wizard)** : a tkinter based interface to easily login to a project, take screenshots, send files to the project repo, this is aim to help adding CAD files, save setups, keep track of every activity of a project which is done on a desktop PC. > run [wizard.py](clients/Wizard/wizard.py)
<!-- 
- OLD **[SatanicBot](clients/bots/SatanicBot)** : Alphabot1, Kevin's repo for his advances on robot displacement on a table

- **[Marcello](clients/bots/Marcello)** : Alphabot2, Clara's repo for her advances on gesture based interaction with the table robot -->

### Capush
start socket server : python3 [capushserver.py](server/capushserver.py)
start a test client : node -r esm [socketclienttest.mjs](clients/socketclienttest.mjs)  (needs esm)
start a manager client on browser: your.local.ip.address:8081/capush
