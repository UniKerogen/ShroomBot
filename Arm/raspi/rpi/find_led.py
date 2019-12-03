
# this is a simple script to find which gpio is the led using
#
import RPi.GPIO as GPIO 
from time import sleep 

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

for i in range(1, 26):
    print("GPI: {}".format(i))
    if (i == 1 or i == 2 or i == 4 or i == 6 or i == 9 or i == 14 or i == 17 or
        i == 20 or i == 25):
        continue
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(i, GPIO.HIGH)
    sleep(1)
    GPIO.output(i, GPIO.LOW) 
    sleep(1)