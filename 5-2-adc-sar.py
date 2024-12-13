import RPi.GPIO as gpio
import sys
from time import sleep


gpio.setmode(gpio.BCM)
dac=[8, 11, 7, 1, 0, 5, 12, 6]
led=[2, 3, 4, 17, 27, 22, 10, 9]
comp=14
troyka=13

gpio.setup(dac, gpio.OUT)
gpio.setup(led, gpio.OUT)
gpio.setup(troyka,gpio.OUT, initial=gpio.HIGH)
gpio.setup(comp, gpio.IN)


def perev(a):
    return [int (elem) for elem in bin(a)[2:].zfill(8)]

def adc():
    ans = [0, 0, 0, 0, 0, 0, 0, 0]
    j = 0
    while True:
        if j == 7:
            break
        ans[j] = 1
        gpio.output(dac, ans)
        sleep(0.001)
        compv = gpio.input(comp)
        if compv == 1:
            ans[j] = 0
        j += 1
    res = sum([ans[7-i] * 2 ** i for i in range(8)])
    return res


try:
    while True:
        k=adc()
        b=k
        leds = [0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        if b == 254:
            leds = [1, 1, 1, 1, 1, 1, 1, 1]
        else:
            while b>32:
                leds[7-i] = 1
                b -= 32
                i+=1
        if k!=0:
            #print(k, '{:.2f}v'.format(3.3*k/256))
            gpio.output(led, leds)
        
finally:
    gpio.output(dac, 0)
    gpio.cleanup()   