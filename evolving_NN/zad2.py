import numpy as np
import matplotlib.pyplot as plt

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
plt.legend(loc='best')
plt.show()
