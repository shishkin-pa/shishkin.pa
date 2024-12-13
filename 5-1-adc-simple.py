import RPi.GPIO as gpio
import sys
from time import sleep


gpio.setmode(gpio.BCM)
dac=[8, 11, 7, 1, 0, 5, 12, 6]
comp=14
troyka=13

gpio.setup(dac, gpio.OUT)
gpio.setup(troyka,gpio.OUT, initial=gpio.HIGH)
gpio.setup(comp, gpio.IN)


def perev(a):
    return [int (elem) for elem in bin(a)[2:].zfill(8)]

def adc():
    for i in range(256):
        v=perev(i)
        gpio.output(dac, v)
        compvalue=gpio.input(comp)
        sleep(0.001)
        if compvalue == 1:
            return i
    return i

p=0

try:
    while True:
            p+=1
            t=adc()
            if p%2!=1:
                print(t, '{:.2f}v'.format(3.3*t/256))
        
finally:
    gpio.output(dac, 0)
    gpio.cleanup()   
