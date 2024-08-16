#!/home/pi/Dispenser/env/bin/python

import json
from paho.mqtt import client as mqtt_client
import random
import os

broker = 'j9a01f0b.ala.dedicated.aws.emqxcloud.com'
port = 1883
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'pi'
password = 'pi'
topic = "71762105028@cit.edu.in/tasks"

path="Dispenser"
os.chdir(path)

def connect():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def loadJSON(filename):
    with open(filename, "r") as JSONFile:
        JSONDict = json.load(JSONFile)
    return JSONDict

def writeJSON(JSONDict, filename):
    with open(filename, "w") as JSONFile:
        json.dump(JSONDict, JSONFile)

def publish(client):
    data = loadJSON("tasks.json")
    for keys in data:
        data[keys] = False
    msg = json.dumps(data)
    writeJSON(data, "tasks.json")
    result = client.publish("71762105028@cit.edu.in/tasks", msg, retain=True)
    status = result[0]
    if status == 0:
        print(f"Send {msg} to topic `{topic} `")
    else:
        print(f"Failed to send message to topic {topic}")



if __name__ == "__main__":
    client = connect()
    client.loop_start()
    publish(client)

