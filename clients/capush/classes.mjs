class CustomEvent extends Event { 
  constructor(message, data = undefined) {
    super(message, data)
    if(data){
        this.detail = data.detail
    }
    else{
        this.detail = undefined
    }
  }
}
class Unit {
    constructor(args){
        this.name = args.name;
        this.type = args.type;
        this.last_location = args.location;
        this.location_time = args.last_location_update;
        this.status = args.status;
        this.status_time = args.last_status_update;
        this.pan = 0.0;
        this.tilt = 0.0;
        this.has_pan_tilt = false;
        this.is_bot = false;
    }
}

class CapushClient extends EventTarget{
    constructor(websocket, client_properties){
        super()
        this.websocket = websocket
        this.websocket.addEventListener('open', () => {
            this.initServerConnection(client_properties )
            console.log('Connected to websocket server.');
            this.dispatchEvent(new CustomEvent('connected'));
        });

        this.websocket.addEventListener("message", ({ data }) => {
            const event = JSON.parse(data);
            switch (event.type) {
             case "unit_list":
                this.dispatchEvent(new CustomEvent('unit_list', {detail: event.message}));
                 break;
             case 'webclient_unit_connect_response':
             this.dispatchEvent(new CustomEvent('webclient_unit_connect_response', {detail: event.message}));
                 break;

             case 'webclient_unit_disconnect_response':  
             this.dispatchEvent(new CustomEvent('webclient_unit_disconnect_response', {detail: event.message}));
                 break;

             default:
                 console.log(event);
                 break;
            }
        });

        this.websocket.addEventListener('error', function (error) {
         this.dispatchEvent(new CustomEvent('error', {detail: error}));
        });

        this.websocket.addEventListener('close', function(event) {
         this.dispatchEvent(new CustomEvent('close', {detail: event}));
        });
    }
    
    initServerConnection(client_properties){
        var msg = {
            'type' : 'init', 'message': client_properties
        }
        console.log("initialiing")
        var request = JSON.stringify(msg);
        this.websocket.send(request);
    }

    query_all_units(){
        var msg = {
            type: 'unit_list_request',
            message: ''
        }
        var request = JSON.stringify(msg);
        this.websocket.send(request);
    }

    unitConnectionRequest(project_name, unit_name){
        var msg_content = {
            project_name : project_name,
            unit_name : unit_name
        }
        var msg = {
            'type' : 'project_unit_connect_request',
            'message': msg_content
        }
        var request = JSON.stringify(msg);
        this.websocket.send(request);
    }

    unitDisconnectionRequest(project_name, unit_name){
        var msg_content = {
            project_name : project_name,
            unit_name : unit_name
        }
        var msg = {
            'type' : 'project_unit_disconnect_request',
            'message': msg_content
        }

        var request = JSON.stringify(msg);
        this.websocket.send(request);
    }
}

class CapushManager extends CapushClient{
    constructor(websocket, client_properties, projectname){
        super(websocket, client_properties)
        this.all_units = {};
        this.available_units = {};
        this.units = {};
        this.projectname = projectname

        this.addEventListener("connected", () => {
            console.log("connected");
        })

        this.addEventListener("unit_list", (units) => {
            this.all_units = units.detail.all;
            this.available_units = units.detail.available;
        
            window.dispatchEvent(new CustomEvent("unit_list", {detail:units.detail}));
        });

        this.addEventListener("webclient_unit_connect_response", (response) => {
            this.handleConnectionReponse(response.detail);
        });
        this.addEventListener("webclient_unit_disconnect_response", (response) => {
            this.handleDisonnectionReponse(response.detail);
        });
        this.addEventListener('error', function (error) {
            console.log('Error connecting to websocket server: ', error.detail);
            this.closeAllSessions();
        });

        this.addEventListener('close', function(event) {
            console.log('Connection to websocket server closed.', event.detail);
            this.closeAllSessions();
        });

    }

    unitDisconnectionRequest(unit_name){
        super.unitDisconnectionRequest(this.projectname, unit_name)
    }

    unitConnectionRequest(unit_name){
        super.unitConnectionRequest(this.projectname, unit_name)
    }

    handleDisonnectionReponse(e){
        if(e.accepted == 1){
            console.log("Connection ended, server says:"+e.msg);
        }else{
            console.log("Disonnection refused, server says:"+e.msg);
        }
    }

    handleConnectionReponse(e){
        if(e.accepted == 1){
            console.log("Connection accepted, server says:"+e.msg);
            if (this.beginSession(e.unit_name)){
                this.dispatchEvent(new CustomEvent('newUnitSession', {detail: this.units[e.unit_name]}));
            }
            else{
                console.log("Connexion failed");
                this.unitDisconnectionRequest(e.unit_name);
            }
        }else{
            console.log("Connection refused, server says:"+e.msg);
        }
    }

    beginSession(unit_name){
        var unit = new Unit(this.all_units[unit_name]);
        this.units[unit_name] = unit; // handling sessions as well
        return true;
    }

    closeSession(unitname){
        this.unitDisconnectionRequest( unitname);
        delete this.units[unitname];
        this.dispatchEvent(new CustomEvent('closingSession', {detail:unitname}));
        console.log("closing session " + unitname);
    }

    closeAllSessions(){
        console.log(this.units);
        var unitnames = Object.keys(this.units);
        console.log(unitnames);

        for (const i in unitnames) {
            var elem = unitnames[i]
            console.log(elem)
            this.closeSession(elem);
        };
    }

    // checkUnitConnections(){ // check if the units used in session are still connected 
    //     var unitnames = Object.keys(this.units);
    //     for (const elem in unitnames) {
    //         console.log(elem)
    //         if(!(elem in this.all_units)){
    //             console.log("Unit: "+elem+" disconnected from server, ending session");
    //             this.closeSession(elem);
    //         }
    //     } 
    // }

}
export {CapushClient, CapushManager}
