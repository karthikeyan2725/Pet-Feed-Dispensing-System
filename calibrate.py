import RPi.GPIO as GPIO
import os
from hx711 import HX711
import pickle

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

DT_PIN = 7
SCK_PIN = 23

hx = HX711(dout_pin = DT_PIN, pd_sck_pin=SCK_PIN)

hx.zero()

input('place known weight on scale and press Enter:')
reading = hx.get_data_mean(readings=100)

known_weight_grams = int(input('Enter Known weight in grams and press enter'))
value = float(known_weight_grams)

ratio = reading/value
hx.set_scale_ratio(ratio)

f = open("ratio.txt","w")
f.write(f"{ratio}")
f.close()

f = open("hx711.pickle","wb")
pickle.dump({"HX711":hx},f)
f.close()

while True:
	weight = hx.get_weight_mean(readings=10)
	print(weight)
