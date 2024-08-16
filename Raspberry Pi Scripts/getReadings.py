import pickle 
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
DT_PIN = 7
SCLK = 23
GPIO.setup(DT_PIN,GPIO.IN)
GPIO.setup(SCLK,GPIO.OUT)
f = open("hx711.pickle","rb")
hx = pickle.load(f)["HX711"]
print(type(hx))
while True:
    print(hx.get_weight_mean(readings=1))
