import matplotlib.pyplot as plt
import numpy

lines = open("params_2x8x3.txt", "r").readlines()

i = 0
toggle = 0

weightsx = []
weightsy = []
for line in lines:
    number = float(line.replace("\n",""))
    if i < 32 and i % 2 == 0:
        if toggle == 0:
            weightsx.append(number)
        else:
            weightsy.append(number)
        toggle = 1 - toggle
    i += 1

# Neural network dataset preparation
# inputs: x, y
# outputs: 100 | 010 | 001
lines = open("zad7-dataset.txt", "r").readlines()
class_100x = []
class_010x = []
class_001x = []
class_100y = []
class_010y = []
class_001y = []
for line in lines:
    values = line.replace("\n","").split("\t")
    if values[2] == '1':
        class_100x.append( float(values[0]) )
        class_100y.append( float(values[1]) )
    elif values[3] == '1':
        class_010x.append( float(values[0]) )
        class_010y.append( float(values[1]) )
    elif values[4] == '1':
        class_001x.append( float(values[0]) )
        class_001y.append( float(values[1]) )
    else:
        raise Exception("invalid example\n" + line)

plt.scatter(class_100x, class_100y, label='class 100')
plt.scatter(class_010x, class_010y, label='class 010')
plt.scatter(class_001x, class_001y, label='class 001')
plt.scatter(weightsx, weightsy, label="weights")
plt.legend(loc='best')
plt.show()
