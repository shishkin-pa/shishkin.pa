import RPi.GPIO as gpio
import sys

dac=[8, 11, 7, 1, 0, 5, 12, 6]

gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT)

def conv(a, n):
    return [int (elem) for elem in bin(a)[2:].zfill(n)]

try:
    while (True):
        a = input('pls input 0-255    ')
        if a=='q':
            sys.exit()
        elif  a.isdigit() and int(a)%1==0 and 0<=int(a)<=255:
            gpio.output(dac, conv(int(a), 8))
            print("{:.4f}".format(int(a)/256*3.3))
            print(int(a)/256*3.3)
        elif not a.isdigit():
            print('pls input INT NUMBER 0-255    ')
        elif not 0<=int(a)<=255:
            print('pls input number FROM 0 TO 255 U STUPID MAGGOT    ')
            
except ValueError:
    print('input number 0-255    ')
except KeyboardInterrupt:
    print('done')
finally:
    gpio.output(dac, 0)
    gpio.cleanup()