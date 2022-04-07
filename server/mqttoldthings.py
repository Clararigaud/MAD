#!/usr/bin/env python3

"""A MQTT to InfluxDB Bridge

This script receives MQTT data and saves those to InfluxDB.

"""

import re
from typing import NamedTuple

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

import sqlite3

import json
with open('../config.json') as json_file:
    data = json.load(json_file)

    INFLUXDB_ADDRESS = data[0]['influxdb_address']
    INFLUXDB_PORT = data[0]['influxdb_port']
    INFLUXDB_USER = data[0]['influxdb_user']
    INFLUXDB_PASSWORD = data[0]['influxdb_pw']
    INFLUXDB_DATABASE = data[0]['influxdb_database']

    MQTT_ADDRESS = data[0]['mosquitto-server-address']
    MQTT_PORT = data[0]['mosquitto-server-port']
    MQTT_USER = data[0]['mosquitto-server-user']
    MQTT_PASSWORD = data[0]['mosquitto-server-pw']


conn = sqlite3.connect('mom.db')
c = conn.cursor()


MQTT_TOPIC = '+/+/+/+'  # [bme280|other]/[temperature|humidity|battery|status]
MQTT_REGEX = '([^/]+)/([^/]+)/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'MQTTInfluxDBBridge'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

class SensorData(NamedTuple):
    lab: str
    station: str
    thing: str
    measurement: str
    value: float

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    #n.notify("WATCHDOG=1")
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
    else:
        print("couldn't parse mqtt message")


def _parse_mqtt_message(topic, payload):
    match = re.match(MQTT_REGEX, topic)
    if match:
        lab = match.group(1)
        station = match.group(2)
        thing = match.group(3)
        measurement = match.group(4)
        if measurement == 'status':
            return None
        return SensorData(lab, station, thing, measurement, float(payload))
    else:
        print('bad message')
        return None

def _send_sensor_data_to_influxdb(sensor_data):
    #print("writing to database" + str(sensor_data.measurement) + " loc:" + str(sensor_data.location) + " val:" + str(sensor_data.value))
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                'lab': sensor_data.lab,
                'station' : sensor_data.station,
                'thing' : sensor_data.thing
            },
            'fields': {
                'value': float(sensor_data.value)
            }
        }
    ]
    influxdb_client.write_points(json_body)


def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)


def main(): 
    _init_influxdb_database()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, MQTT_PORT, 60)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    # n = sdnotify.SystemdNotifier()
    # n.notify("READY=1")
    main()
