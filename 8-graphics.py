from matplotlib import pyplot
import numpy
from textwrap import wrap
import matplotlib.ticker as ticker

with open('settings.txt') as file:
    settings=[float(i) for i in file.read().split('\n')]


#считываем показания компаратора и переводим через шаг квантования в вольиты
data=numpy.loadtxt('data.txt', dtype=int) * settings[1]

#массив времен, создаваемый черед количество измерений и известный шаг по времени
data_time=numpy.array([i*settings[0] for i in range(data.size)])

#параметры фигуры
fig, ax=pyplot.subplots(figsize=(16, 10), dpi=500)



#минимальные и максимальные значения для осей
ax.axis([data_time.min(), data_time.max(), data.min(), data.max()+0.2])


#  Устанавливаем интервал основных делений:
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.005))
#  Устанавливаем интервал вспомогательных делений:
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.001))



#  Тоже самое проделываем с делениями на оси "y":
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))


#название графика с условием для переноса строки и центрированием
ax.set_title("\n".join(wrap('Процесс заряда и разряда конденсатора в RC цепи', 60)), loc = 'center')


#сетка основная и второстепенная
ax.grid(which='major', color = 'gray')
ax.minorticks_on()
ax.grid(which='minor', color = 'gray', linestyle = ':')


#подпись осей
ax.set_ylabel("Напряжение, В")
ax.set_xlabel("Время, с")


#линия с легендой
ax.plot(data_time, data, c='black', linewidth=1, label = 'U(t)')
ax.scatter(data_time[0:data.size:20], data[0:data.size:20], marker = '*', c = 'g', s=40)
ax.legend(shadow = False, loc = 'right', fontsize = 30)

#время зарядки/разрядки
str1='Время зарядки: ' + str(round(data_time.max()+0.2, 4)) + ' с'
pyplot.text(0.64, 0.4, str1 , fontsize=24, transform=ax.transAxes, bbox=dict(facecolor='g', alpha=0.2))
str2='Время разрядки нельзя посчитать, т.к. конденсатор разряжается не до конца'
pyplot.text(0.43, 0.35, str2, fontsize=12, transform=ax.transAxes, bbox=dict(facecolor='g', alpha=0.2))


#сохранение
fig.savefig('graph.png')
fig.savefig('graph.svg')
