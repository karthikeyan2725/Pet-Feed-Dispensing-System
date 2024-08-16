#!/home/pi/Dispenser/env/bin/python

import json
from crontab import CronTab
from datetime import time
import os

cron = CronTab(user = True)

path = "/home/pi/Dispenser"
os.chdir(path)

def enablePermissions():
    files = ["openDispenser.py", "subscriber.py", "clearTasks.py"]

    for file in files:
        os.chmod(file, 0o555)


def setClearTasks():
    with open("config.json") as file:
        configDict = json.load(file)

    job = next(cron.find_comment(f"{configDict['email']}/tasks"), None)
    if job is None:
        job = cron.new(command = './Dispenser/clearTasks.py')
        job.set_comment(f"{configDict['email']}/tasks")
        job.setall(time(0, 0))
        cron.write()


def setMainTasks():
    with open("config.json") as file:
        configDict = json.load(file)

    job = next(cron.find_comment(f"{configDict['email']}/main"), None)
    if job is None:
        job = cron.new(command = 'sleep 30 && ./Dispenser/subscriber.py')
        job.set_comment(f"{configDict['email']}/main")
        job.every_reboot()
        cron.write()


if __name__ == '__main__':
    enablePermissions()
    setMainTasks()
    setClearTasks()
