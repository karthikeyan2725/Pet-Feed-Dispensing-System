#!/home/pi/Dispenser/env/bin/python
from stepper_module import move
from time import sleep
import pickle
import RPi.GPIO as GPIO
from hx711 import HX711
from datetime import datetime
from paho.mqtt import client as mqtt_client
import json
import sys
import os

path="Dispenser"
mapper = {'night':'morning', 'morning':'afternoon', 'afternoon':'night'}
os.chdir(path)


def feed(weight,time):

    f = open(f"state.txt","r+")
    g = open(f"hx711.pickle","rb")
    j = open(f"saved.json","r+")

    saved_json = json.load(j)
    j.truncate(0)
    j.seek(0)
    print(f.read().split())
    state = "closed"
    DT_PIN = 7
    SCK_PIN = 23
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SCK_PIN,GPIO.OUT)
    GPIO.setup(DT_PIN,GPIO.IN)
    
    hx = HX711(dout_pin=DT_PIN,pd_sck_pin=SCK_PIN)
    data = pickle.load(g)
    hx = data["HX711"]
    g.close()
    
    curr = hx.get_weight_mean(1)
    percent = int(((weight-curr)/weight)*100) if curr >=0 else 0
    print(f"current = {curr}")
    print(f"{weight-curr}, {weight},{percent}")
    if time in saved_json:
        saved_json[time].append(percent)
    else:
        saved_json[time] = [percent]


    send(saved_json)
    with open("tasks.json", "r") as file:
        task_data = json.load(file)
        task_data[mapper[time]] = True
        send(task_data, "71762105028@cit.edu.in/tasks")
    with open("tasks.json", "w") as file:
        json.dump(task_data, file)
    json.dump(saved_json,j)
    j.close()

    with open("logging.txt", "a") as file:
        file.writelines(f"opened {datetime.now()}\n")

    if state == "closed":
        f.truncate(0)
        f.seek(0)
        f.write("open")
        move("c")
        curr = hx.get_weight_mean(1)
        while curr < weight - 5:
            curr = hx.get_weight_mean(1)
            print(curr)
        move("a")
        f.truncate(0)
        f.seek(0)
        f.write("closed")
        f.close()
        return 1
    else:
        f.close()
        return 0


def send(data, topic="71762105028@cit.edu.in/weight"):
    host = 'j9a01f0b.ala.dedicated.aws.emqxcloud.com'
    port = 1883
    username = 'pi'
    password = 'pi'
    
    def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client()
        #client.tls_set(ca_certs='./emqxsl-ca.crt')
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(host, port)
        return client

    def publish(client):
        msg = json.dumps(data)
        result = client.publish(topic, msg, retain=True)
        status = result[0]
        if status == 0:
            print(f"Send {msg} to topic `{topic} `")
        else:
            print(f"Failed to send message to topic {topic}")
            
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == "__main__":
    with open("tasks.json") as file:
        configDict = json.load(file)

        if not configDict[mapper[sys.argv[2]]]:
            feed(int(sys.argv[1]),sys.argv[2])    
