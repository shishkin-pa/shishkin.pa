import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.IN)

for i in range (100000):
    GPIO.output(21, GPIO.input(20))    
    time.sleep(0.1)