import RPi.GPIO as gpio
import time
from matplotlib import pyplot

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

leds=[2, 3, 4, 17, 27, 22, 10, 9]
gpio.setup(leds, gpio.OUT)

dac=[8, 11, 7, 1, 0, 5, 12, 6]
gpio.setup(dac, gpio.OUT, initial=gpio.HIGH)

comp=14
troyka=13 
gpio.setup(troyka,gpio.OUT, initial=gpio.HIGH)
gpio.setup(comp, gpio.IN)



#снятие показаний с тройки
def adc():
    k=0
    for i in range(7, -1, -1):
        k+=2**i
        gpio.output(dac, perev(k))
        time.sleep(0.004)
        if gpio.input(comp)==1:
            k-=2**i
    return k



#перевод в двоичную
def perev(a):
    return [int (elem) for elem in bin(a)[2:].zfill(8)]



try:
    napr=0
    results=[]
    time_start=time.time()
    count=0
    q=0


    #зарядка конденсатора, запись показаний в процессе
    print('начало зарядки конденсатора')
    while napr < 190:
        napr=adc()
        print(napr)
        results.append(napr)
        # time.sleep(0.001)
        count+=1
        gpio.output(leds, perev(napr))


    gpio.setup(troyka,gpio.OUT, initial=gpio.LOW)


    #разрядка конденсатора, запись показаний в процессе
    print('начало разрядки конденсатора')
    while napr>165:
        napr=adc()
        print(napr)
        results.append(napr)
        time.sleep(0)
        count+=1
        gpio.output(leds, perev(napr))


    time_experiment=time.time()-time_start


    #запись данных в файлы
    print('запись данных в файл')
    with open('data.txt', 'w') as f:
        for i in results:
            f.write(str(i) + '\n')
    with open('settings.txt', 'w') as f:
        f.write(str(1/time_experiment/count) + '\n')
        f.write('0.01289')
    

    print('общая продолжительность эксперимента {}, период одного измерения {}, средняя частота дискретизации {}, шаг квантования АЦП {}'.format(time_experiment, time_experiment/count, 1/time_experiment/count, 0.013))


    #графики
    print('построение графиков')
    y=[i/256*3.3 for i in results]
    x=[i*time_experiment/count for i in range(len(results))]
    pyplot.plot(x, y)
    pyplot.xlabel('время')
    pyplot.ylabel('вольтаж')
    pyplot.show()



finally:
    gpio.output(leds, 0)
    gpio.output(dac, 0)
    gpio.cleanup()