#!/home/pi/Dispenser/env/bin/python


import random
import json
from paho.mqtt import client as mqtt_client
from crontab import CronTab
from datetime import time



cron = CronTab(user = True)
broker = 'j9a01f0b.ala.dedicated.aws.emqxcloud.com'
port = 1883
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'pi'
password = 'pi'

mapping = {'morning':'night', 'afternoon':'morning', 'night':'afternoon'}

def NewJob(configDict, course):
    job = cron.new(command = f"./Dispenser/openDispenser.py 50 {mapping[course]}")
    job.set_comment(f"{configDict['email']}/{course}")
    return job

def updateCrobJobs(configDict):

    for course in ["morning", "afternoon", "night"]:
        job = next(cron.find_comment(f"{configDict['email']}/{course}"), None)

        if job is None:
            job = NewJob(configDict, course)

        job.setall(time(configDict[course]['hour'], configDict[course]['minutes']))
        cron.write()

def loadJSON(filename):
    with open(filename, "r") as JSONFile:
        JSONDict = json.load(JSONFile)
    return JSONDict

def writeJSON(JSONDict, filename):
    with open(filename, "w") as JSONFile:
        json.dump(JSONDict, JSONFile)


def connect_mqtt() -> mqtt_client:
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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        email, course = msg.topic.split("/")
        updatedTime = json.loads(msg.payload.decode())

        configDict = loadJSON("config.json")
        configDict[course] = updatedTime
        writeJSON(configDict, "config.json")
        updateCrobJobs(configDict)




    configDict = loadJSON("config.json")

    for course in ["morning", "afternoon", "night"]:
        client.subscribe(f"{configDict['email']}/{course}")

    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
