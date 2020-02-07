import random
import math
import subprocess
import numpy
import sys

training_algorithm = sys.argv[1]

class NeuralNetwork:
    LEARNING_RATE = 0.6
    INERTION_RATE = 0.4
    
    def __init__(self, architecture):
        self.architecture = architecture 
        self.layers = []
        self.num_layers = len(architecture) - 1
        self.num_inputs = architecture[0]
        for i in range(1, len(architecture)):
            self.layers.append(NeuronLayer(self.architecture[i], self.architecture[i-1]))

    def inspect(self):
        print('#'*30)
        print('Number of input neurons ', self.num_inputs)
        print('#'*30)
        for i in range(self.num_layers):    
            self.layers[i].inspect()
            print('#'*30)

    def feed_forward(self, inputs):
        food = inputs
        for i in range(self.num_layers):
            food = self.layers[i].feed_forward(food)
        return food 
    
    # weights are modified only after all training examples are seen (full gradient is calculated)              
    def batch_learning_train(self, training_inputs, target_outputs):
        # for each training input
        for X in range(len(training_inputs)):
            self.feed_forward(training_inputs[X])
            # calculate error function weight gradients on output layer
            # for each output layer neuron
            for j in range(len(self.layers[self.num_layers-1].neurons)):
                # for each of those neurons weight
                for i in range(self.layers[self.num_layers-1].neurons[j].num_inputs):
                    delta = self.layers[self.num_layers-1].neurons[j].calculate_delta(self.num_layers, self.layers, self.num_layers-1, j, target_outputs[X])
                    self.layers[self.num_layers-1].neurons[j].weight_adjustment_value[i] += ( delta * self.layers[self.num_layers-1].neurons[j].inputs[i] ) 
            
            # calculate error function weight gradients on hidden layers
            j = self.num_layers - 2
            # for each hidden layer
            while j >= 0:
                # for each neuron in hidden layer
                for i in range(len(self.layers[j].neurons)):
                     # for each of those neurons weight
                    for k in range(self.layers[j].neurons[i].num_inputs):
                        delta = self.layers[self.num_layers-1].neurons[j].calculate_delta(self.num_layers, self.layers, j, i, target_outputs[X])
                        self.layers[j].neurons[i].weight_adjustment_value[i] += ( delta * self.layers[j].neurons[i].inputs[i] ) 
                j -= 1
                
        # all training examples seen
        # adjust weight on all neurons
        for i in range(self.num_layers):
            for j in range(len(self.layers[i].neurons)):
                for k in range (len(self.layers[i].neurons[j].inputs)):
                    self.layers[i].neurons[j].weights[k] = self.layers[i].neurons[j].weight_adjustment_value[k] * self.LEARNING_RATE
                        
    # weights are modified immeadiately upon calculating gradient approximation for that weight                
    def online_learning_train(self, training_inputs, target_outputs):
        # for each training input
        for X in range(len(training_inputs)):
            self.feed_forward(training_inputs[X])
            # calculate error function weight gradients on output layer
            # for each output layer neuron
            for j in range(len(self.layers[self.num_layers-1].neurons)):
                # for each of those neurons weight
                for i in range(self.layers[self.num_layers-1].neurons[j].num_inputs):
                    delta = self.layers[self.num_layers-1].neurons[j].calculate_delta(self.num_layers, self.layers, self.num_layers-1, j, target_outputs[X])
                    # adjust weight based on gradient approximation
                    self.layers[self.num_layers-1].neurons[j].last_weight_change = self.LEARNING_RATE * ( delta * self.layers[self.num_layers-1].neurons[j].inputs[i] )  + self.INERTION_RATE * self.layers[self.num_layers-1].neurons[j].last_weight_change
                    self.layers[self.num_layers-1].neurons[j].weights[i] += self.layers[self.num_layers-1].neurons[j].last_weight_change
                    
            # calculate error function weight gradients on hidden layers
            j = self.num_layers - 2
            # for each hidden layer
            while j >= 0:
                # for each neuron in hidden layer
                for i in range(len(self.layers[j].neurons)):
                     # for each of those neurons weight
                    for k in range(self.layers[j].neurons[i].num_inputs):
                        delta = self.layers[self.num_layers-1].neurons[j].calculate_delta(self.num_layers, self.layers, j, i, target_outputs[X])
                        # adjust weight based on gradient approximation
                        self.layers[j].neurons[i].last_weight_change = self.LEARNING_RATE *( delta * self.layers[j].neurons[i].inputs[i] ) + self.INERTION_RATE * self.layers[j].neurons[i].last_weight_change
                        self.layers[j].neurons[i].weights[i] += self.layers[j].neurons[i].last_weight_change
                j -= 1
                
                    
    def calculate_total_error(self, training_sets):
        total_error = 0
        for t in range(len(training_sets)):
            training_inputs, training_outputs = training_sets[t]
            self.feed_forward(training_inputs)
            for o in range(len(training_outputs)):
                total_error += self.layers[self.num_layers-1].neurons[o].calculate_error(training_outputs[o])
        self.total_error = total_error
        return total_error

class NeuronLayer:
    def __init__(self, num_neurons, num_weights):

        self.neurons = []
        self.num_weights = num_weights
        for i in range(num_neurons):
            self.neurons.append(Neuron(self.num_weights))
            
    def inspect(self):
        print('Neurons:', len(self.neurons))
        
        #for n in range(len(self.neurons)):
            #print(' Neuron', n)
            #for w in range(len(self.neurons[n].weights)):
                #print('  Weight:', self.neurons[n].weights[w])

    def feed_forward(self, inputs):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.calculate_output(inputs))
        return outputs

    def get_outputs(self):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.output)
        return outputs
            
class Neuron:
    def __init__(self, num_inputs):
        self.weights = []
        self.num_inputs = num_inputs
        self.weight_adjustment_value = [0.0 for i in range(num_inputs)]
        self.last_weight_change = 0
        #self.deltas = [0.0 for i in range(num_inputs)]
        for i in range(self.num_inputs):
            self.weights.append(random.random())
            
    def calculate_output(self, inputs):
        self.inputs = inputs
        self.output = self.squash(self.calculate_total_net_input())
        return self.output

    def calculate_total_net_input(self):
        total = 0
        for i in range(len(self.inputs)):
            total += self.inputs[i] * self.weights[i]
        return total
    
    # used when OverflowError occurs in squash function
    def exp_normalize(self, x):
        b = x.max()
        y = numpy.exp(x - b)
        return y / y.sum()
    # logistic function
    def squash(self, total_net_input):
        try:    
            return 1 / (1 + numpy.exp(-total_net_input))
        except OverflowError:
            return 1 / (1 + exp_normalize(-total_net_input))
            
    # The error for each neuron is calculated by the Mean Square Error method:
    def calculate_error(self, target_output):
        return 0.5 * (target_output - self.output) ** 2

    # recursive function used for calculating error in batch learning algorithm
    # num_layers - numbar of layers in network
    # layers     - self.layers
    # layer      - which layer is current
    # index      - index in neuron layer
    # target_output
    def calculate_delta(self, num_layers, layers, layer, index, target_output):
        #print(index)
        if layer == num_layers-1:
            return self.output * (1 - self.output) * (target_output[index] - self.output)
        else:
            suma = 0.0
            for i in range(len(layers[layer+1].neurons)):
                suma += layers[layer+1].neurons[i].calculate_delta(num_layers, layers, layer+1, i, target_output) * layers[layer+1].neurons[i].weights[index]
            
            return self.output * (1 - self.output) * suma    
    
            
        
###
FOLDER = "./learningdata/20tocaka/"
#FOLDER = sys.argv[1]
# prepare learning data
train_set = []
inputs = []
outputs = []
number_of_inputs = 0
names = [ "alfa", "beta", "gama", "delta", "epsilon" ]    
for name in names:
    for i in range(1,21):
        number = "{:0>2d}".format(i)
        filename = name + number
        data = open(FOLDER + filename, "r").readlines()
        inp = []
        number_of_inputs = len(data)*2
        for line in data:    
            x,y = line.replace("\n","").split(" ")
            inp.append(float(x))
            inp.append(float(y))
            
        inputs.append(inp)
        out = [0,0,0,0,0]
        out[ names.index(name) ] = 1
        outputs.append(out)

        train_set.append([inp, out])


        
batch_inputs = [ [] for i in range(10) ]
batch_outputs = [ [] for i in range(10) ]
batch_size = 10
batch_count = 0
for i in range(1,21):        
    for name in names:
             
        number = "{:0>2d}".format(i)
        filename = name + number
        data = open(FOLDER + filename, "r").readlines()
        temp_input = []
        number_of_inputs = len(data)*2
        for line in data:    
            x,y = line.replace("\n","").split(" ")
            temp_input.append(float(x))
            temp_input.append(float(y))
        out = [0,0,0,0,0]
        out[ names.index(name) ] = 1
        
        batch_inputs[batch_count // batch_size].append(temp_input)
        batch_outputs[batch_count // batch_size].append(out)
        batch_count += 1
        
architecture = [number_of_inputs]
if len(sys.argv) <= 4:
    print("Usage: python3 neural-network.py [batch|online|minibatches] hidden_layer1_num ... output_layer_num ")
    exit()
    
for i in range(2, len(sys.argv)):
    architecture.append(int(sys.argv[i]))
nn = NeuralNetwork(architecture) 
nn.inspect()
learn_count = 0
while True:
    if training_algorithm == "batch":
        nn.batch_learning_train(inputs, outputs)
    elif training_algorithm == "online":
        nn.online_learning_train(inputs, outputs)
    elif training_algorithm == "minibatches":
        for i in range(len(batch_inputs)):
            nn.batch_learning_train(batch_inputs[i], batch_outputs[i])
    else:
        print("Usage: python3 neural-network.py [batch|online|minibatches] hidden_layer1_num ... output_layer_num ")
        exit()
    total_error = nn.calculate_total_error(train_set)
    print(learn_count, total_error)
    learn_count += 1
    if total_error < 10 or learn_count == 1000:
        break

#nn.inspect()

while True:
    subprocess.run(["python", "./draw.py",  str(number_of_inputs // 2), "test"])
    test_data = open("test", "r").readlines()
    test_input = []
    for line in test_data:
        x,y = line.replace("\n", "").split(" ")
        test_input.append(float(x))
        test_input.append(float(y))
    
    print(nn.feed_forward(test_input))
