import {CapushManager} from '../classes.mjs';
var client_properties = {'client_type': 'manager', "has_screen": true, "has_trigger": true, "location": undefined, "has_camera": false}; 
var tags = []; // TODO figure out what to do with them tags
var client = new CapushManager(new WebSocket("ws://localhost:8001/"), client_properties, "clara");

// maybe nicer way to do this but I' m  not a JS pro
client.addEventListener("newUnitSession", function(event){
	window.dispatchEvent(new CustomEvent('newUnitSession', {detail: event.detail}));
});

client.addEventListener("closingSession", function(event){
	window.dispatchEvent(new CustomEvent('closingSession', {detail: event.detail}));
});

window.addEventListener('beforeunload', function(){
	client.closeAllSessions();
});

window.addEventListener('unitConnectionRequest', function(event){
	client.unitConnectionRequest(event.detail.unit_name);
});

window.addEventListener('unitDisconnectionRequest', function(event){
	if(event.detail.unit_name == 'all'){
		client.closeAllSessions();
	}
	else{
		client.closeSession(event.detail.unit_name)
	}
});