import matplotlib.pyplot as plt
import numpy

# testing neuron1 output function for w = 2 and different s
def neuron1_output_function(x, s):
    return 1 / (1 + abs(x - 2) / abs(s))

# domain
x = numpy.linspace(-8, 10)

for s in [1, 0.25, 4]:
    plt.plot(x, neuron1_output_function(x, s), label="s : " + str(s))

plt.legend(loc='best')
plt.show()
