#!/usr/bin/env node
import {CapushClient} from './classes.mjs';
import WebSocket from 'ws'
var clientproperties = {'client_type': 'unit', 'unit_name': 'fufu', "has_screen": false, "has_trigger": false, "location": undefined, "has_camera": false}
var client = new CapushClient(new WebSocket("ws://localhost:8001/"), clientproperties);
client.addEventListener("connected", () => {
	console.log("connected");
})