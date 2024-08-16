import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)

pins = (29,31,33,35) 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pins,GPIO.OUT)

s1 = (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW)
s2 = (GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW)
s3 = (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW)
s4 = (GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH)

sleep_time = 0.01
n = 50
while True:
    dir = input(">")
    
    if dir == "l":
        for i in range(n):
            for s in (s4,s3,s2,s1):
                GPIO.output(pins,s)
                sleep(sleep_time)
                
    elif dir == "r":
        for i in range(n):
            for s in (s1,s2,s3,s4):
                GPIO.output(pins,s)
                sleep(sleep_time)
                
    print(f"Running {i}")
