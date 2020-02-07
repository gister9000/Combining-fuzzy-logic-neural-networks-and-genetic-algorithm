import numpy
import random
import time
import sys
import math

### NEURAL NETWORK PARAMETERS
architecture = [int(sys.argv[1]), int(sys.argv[2])]
dimension = architecture[0] * 2 * architecture[1] 
best_params_filename = "params_" + sys.argv[1] + "x" + sys.argv[2]
for i in range(3, len(sys.argv)):
    architecture.append(int(sys.argv[i]))
    dimension += (architecture[i-2]+1) * architecture[i-1]
    best_params_filename += "x" + sys.argv[i]
print("Architecture", architecture, "needs", dimension, "parameters")
best_params_filename += ".txt"
print("Chromosomes dimension (number of params in NN): ", dimension)

# Neural network dataset preparation
# inputs: x, y
# outputs: 100 | 010 | 001
lines = open("zad7-dataset.txt", "r").readlines()
data = []
for line in lines:
    values = line.replace("\n","").split("\t")
    data.append( [ float(values[i]) for i in range(len(values)) ] )  

training_sets = []
for testcase in data:
    training_sets.append([testcase[0:2],testcase[2:5]])

###
# GENETIC ALGORITHM PARAMETERS
elitism = True
lower_limit = -0.5
upper_limit = 0.5
generation_count_limit = 1e5 
epsilon = 0.03
k = 3 # k-tournament k; increasing this makes children better, but at great speed cost; 3 is the best
population_size = 31 # increasing this makes convergence faster, but at a cost of 
mutation_probability = 0.15   # reduces local optimum problems, but worsens children quality
crossover_probability = 0.7  
seconds = 300000
# float comparer
def isclose(a, b):
    return abs(a-b) <= epsilon

# floating point chromosomes
class chromosome:
        def __init__(self, dimension, empty=False):
                self.badness = 0.0
                self.dimension = dimension
                if empty is False:
                        self.values = [random.uniform(lower_limit, upper_limit) for i in range(dimension)]
                else:
                        self.values = []
                        for i in range(dimension):
                                self.values.append(0.0)
                                
        def __str__(self):
                s = "#" * 100 + "\n"
                for item in self.values:
                        s += str(item) + "  "
                s += "\nBadness: " + str(self.badness)               
                return s

        def __eq__(self, other):
                equal = True
                for i in range(len(self.values)):
                        if isclose(self.values[i], other.values[i]) is False:
                                equal = False
                                break
                return equal

class population:
        def __init__(self, size, dimension, empty=False):
                self.chromosomes = []
                self.iterator = 0
                self.size = size
            
                if empty is False:
                        for i in range(size):
                             self.chromosomes.append(chromosome(dimension))
                else:
                        for i in range(size):
                             self.chromosomes.append(chromosome(dimension, empty=True))

        def __iter__(self):
                return self

        def __next__(self):
                if self.iterator >= self.size:
                        self.iterator = 0
                        raise StopIteration
                else:
                        self.iterator += 1
                        return self.chromosomes[self.iterator - 1]

        def __str__(self):
                s = ""
                for item in self.chromosomes:
                        s += str(item) + "\n"             
                return s

        def __len__(self):
                return self.size        
        
        def sort(self):
                self.chromosomes.sort(key=lambda x: x.badness)

# class that contains recombination and mutation algorithms
class genetic_algorithm:
        def choose_parent_ktournament(p, k):
                possible_parents = [random.choice(p.chromosomes) for i in range(k)]
                possible_parents.sort(key=lambda x: x.badness)
                return possible_parents[0]

        # mean squared error sum for all cases
        def evaluate_individual(c, nn, training_sets):
            c.badness = nn.calculate_total_error(training_sets, parameters=c.values)
            return c.badness

        # returns 2 children created by arithmetic recombination of parents
        def simple_arithmetic_recombination_2(crossover_probability, parent1, parent2):
                child1 = chromosome(parent1.dimension)
                child2 = chromosome(parent1.dimension)
                if random.uniform(0,1) <= crossover_probability:
                        x_point = random.randint(0, len(parent1.values) - 1)
                        for i in range(x_point):
                                child1.values[i] = parent1.values[i]
                                child2.values[i] = (parent2.values[i] + parent1.values[i]) / 2
                        for i in range(x_point, len(parent1.values)):
                                child1.values[i] = (parent1.values[i] + parent2.values[i]) / 2
                                child2.values[i] = parent2.values[i]
                else:
                        for i in range(0, len(parent1.values)-1):
                                child1.values[i] = parent1.values[i]
                                child2.values[i] = parent2.values[i]
                return child1, child2
                
        # returns 2 children created by heuristic recombination of parents     
        def simple_heuristic_recombination_2(crossover_probability, parent1, parent2):
                child1 = chromosome(parent1.dimension)
                child2 = chromosome(parent1.dimension)
                if random.uniform(0,1) <= crossover_probability:
                        for i in range(parent1.dimension):
                                child1.values[i] = random.uniform(parent1.values[i], parent2.values[i])              
                                child2.values[i] = random.uniform(parent1.values[i], parent2.values[i]) 
                else:
                        for i in range(0, len(parent1.values)-1):
                                child1.values[i] = parent1.values[i]
                                child2.values[i] = parent2.values[i]
                return child1, child2
        
       
        def better_parent_crossover(crossover_probability, parent1, parent2):
            child1 = chromosome(parent1.dimension)
            if parent1.badness < parent2.badness:
                child1.values = parent1.values
            else:
                child1.values = parent2.values
            return child1


                        
        # returns 2 children created by heuristic recombination of parents     
        def simple_heuristic_recombination_2(crossover_probability, parent1, parent2):
                child1 = chromosome(parent1.dimension)
                child2 = chromosome(parent1.dimension)
                if random.uniform(0,1) <= crossover_probability:
                        for i in range(parent1.dimension):
                                child1.values[i] = random.uniform(parent1.values[i], parent2.values[i])              
                                child2.values[i] = random.uniform(parent1.values[i], parent2.values[i]) 
                else:
                        for i in range(len(parent1.values)):
                                child1.values[i] = parent1.values[i]
                                child2.values[i] = parent2.values[i]
                return child1, child2
       
        def add_gauss_mutation(mutation_probability, c):
                for i in range(len(c.values)):
                    if random.uniform(0,1) <= mutation_probability:
                        c.values[i] += random.gauss(0, 0.4)
                        
        def set_gauss_mutation(mutation_probability, c): 
                for i in range(len(c.values)):
                    if random.uniform(0,1) <= mutation_probability:
                        c.values[i] = random.gauss(0, 2)
                     
        
# function that performs genetic algorithm
def GA_generation(population_size, nn, dimension, mutation_probability, crossover_probability, dataset, seconds, resume=None):
        # performance measurement
        start = time.time()
        number_of_function_eval = 0
        
        populationX = population(population_size, dimension, empty=False)
        new_generation = population(population_size, dimension, empty=False)

        if resume:
            populationX.chromosomes[0].values = [ float(line.replace("\n","")) for line in open(resume,"r").readlines() ]
            input("loading from " + resume + "\nEnter to continue")
            print(populationX.chromosomes[0].values)
        training_sets = []
        for testcase in dataset:
            training_sets.append([testcase[0:2],testcase[2:5]])
        for item in populationX:
                genetic_algorithm.evaluate_individual(item, nn, training_sets) 
                number_of_function_eval += 1
                     
        populationX.sort()
        best_chromosome = populationX.chromosomes[0]
        count = 0
        while True:
                count += 1
                num_of_elites = 0
                if elitism == True:
                    new_generation.chromosomes[0] = best_chromosome
                    # 1 chromosome survives every time
                    num_of_elites = 1

                for i in range(num_of_elites, population_size // 2):
                        parent1 = genetic_algorithm.choose_parent_ktournament(populationX, k)
                        parent2 = genetic_algorithm.choose_parent_ktournament(populationX, k)
                        
                        algorithm_pick = random.randint(0,1) 
                        if algorithm_pick == 0:
                            child1, child2 = genetic_algorithm.simple_arithmetic_recombination_2(crossover_probability, parent1, parent2)
                        elif algorithm_pick == 1:
                            child1, child2 = genetic_algorithm.simple_heuristic_recombination_2(crossover_probability, parent1, parent2)
                         
                        if random.random() >= mutation_probability:
                            genetic_algorithm.add_gauss_mutation(mutation_probability, child1)
                            genetic_algorithm.add_gauss_mutation(mutation_probability, child2)
                        else:                        
                            genetic_algorithm.set_gauss_mutation(mutation_probability, child1)
                            genetic_algorithm.set_gauss_mutation(mutation_probability, child2)
                        
                        new_generation.chromosomes[2*i-1] = child1
                        new_generation.chromosomes[2*i] = child2
                        
                # old generation dies
                populationX = new_generation
                for item in populationX:
                        genetic_algorithm.evaluate_individual(item, nn, training_sets)
                        number_of_function_eval += 1        
                populationX.sort()
                
                if populationX.chromosomes[0].badness < best_chromosome.badness:
                    print(50*"#" + "\nGeneration #" + str(count), end = "\t")
                    print(populationX.chromosomes[0].badness)
                    print("Time in seconds: ", time.time() - start)
                best_chromosome = populationX.chromosomes[0]        
                #print(best_chromosome)
                # when to stop
                if abs(best_chromosome.badness) <= epsilon or time.time() - start > seconds:
                        print("DONE!!\n")
                        print("Time in seconds: ", time.time() - start)
                        print("Number of function evaluations: ", number_of_function_eval)
                        log = open(best_params_filename, "w")
                        for value in best_chromosome.values:
                            log.write(str(value) + "\n")
                        log.close()
                        print(best_chromosome)
                        
                        return best_chromosome.values
                if count >= generation_count_limit:
                        print("Generation count limit exceeded!!!")
                        print("Time in seconds: ", time.time() - start)
                        print("Number of function evaluations: ", number_of_function_eval)
                        break  
            

    
class NeuralNetwork:
    def __init__(self, architecture, number_of_params, params=None):
        
        self.architecture = architecture 
        self.layers = []
        self.num_layers = len(architecture) - 1
        self.num_inputs = architecture[0]
        # first hidden layer has type 1 neurons
        self.layers.append(NeuronLayer(self.architecture[1], self.architecture[0], 1))
        # other hidden layers have type 2 neurons
        self.number_of_params = number_of_params
        self.params = []
          
        for i in range(2, len(architecture)):
            self.layers.append(NeuronLayer(self.architecture[i], self.architecture[i-1], 2))
        if params:
            print("Loading " + params)
            params_file = open(params, "r").readlines()
            for line in params_file:
                self.params.append(float(line.replace("\n","")))
            self.set_parameters(self.params)      
            
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
            if i == self.num_layers - 1: 
               food = self.layers[i].feed_forward(food)
            else:
               food = self.layers[i].feed_forward(food)
        return food 
    
    def calc_output_with_parameters(self, inputs, parameters):
        self.set_parameters(parameters)
        return self.feed_forward(inputs)
        
    # sets params from helper list to actual weights and other
    def set_parameters(self, parameters):
        if len(parameters) != self.number_of_params:
            raise Exception('len(parameters) must be ' + str(self.number_of_params))
        self.params = parameters
        count = 0
        for i in range(self.num_layers):
            for j in range(len(self.layers[i].neurons)):
                if i != 0:
                    self.layers[i].neurons[j].bias = self.params[count]
                    count += 1
                for k in range(len(self.layers[i].neurons[j].weights)):
                    self.layers[i].neurons[j].weights[k] = self.params[count]
                    count += 1
                    if i == 0:
                        self.layers[i].neurons[j].s[k] = self.params[count]
                        count += 1
       
        if count != self.number_of_params:
            raise Exception("some params have not been set, count = " + str(count))
        
    def calculate_total_error(self, training_sets, parameters=None):
        if parameters:
            self.set_parameters(parameters)
        else:
            print(self.params)
            input("Calculating error with preset parameters. Press ENTER to continue")
        total_error = 0
        for t in range(len(training_sets)):
            training_inputs, training_outputs = training_sets[t]
            self.feed_forward(training_inputs)
            for o in range(len(training_outputs)):
                total_error += self.layers[self.num_layers-1].neurons[o].calculate_error(training_outputs[o])
        self.total_error = total_error
        return total_error / len(training_sets)
    
# Neuron layer, both types supported
class NeuronLayer:
    def __init__(self, num_neurons, num_weights, neuron_type):

        self.neurons = []
        self.num_weights = num_weights
        for i in range(num_neurons):
            if neuron_type == 1:
                self.neurons.append(Neuron1(self.num_weights))
            elif neuron_type == 2:
                self.neurons.append(Neuron2(self.num_weights))
                        
    def inspect(self):
        print("Neurons:", len(self.neurons))     
        
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
        
    
class Neuron2:
    def __init__(self, num_inputs):
        self.weights = []
        self.bias = random.uniform(-1,1)
        self.num_inputs = num_inputs
        for i in range(self.num_inputs):
            self.weights.append(random.uniform(-0.5,0.5))
            
    def calculate_output(self, inputs, output_layer=False):
        self.inputs = inputs
        self.output = self.squash(self.calculate_total_net_input())     
        return self.output

    def calculate_total_net_input(self):
        suma = 0
        for i in range(len(self.inputs)):
            suma += self.inputs[i] * self.weights[i]
        return suma + self.bias
    
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
        return 0.5 * ((target_output - self.output) ** 2)

   
    
# neurons placed only on first hidden layer
class Neuron1:
    def __init__(self, num_inputs):
        self.weights = []
        self.s = []
        self.num_inputs = num_inputs
        for i in range(self.num_inputs):
            self.weights.append(random.uniform(-0.5,0.5))
            self.s.append(random.uniform(-0.5,0.5))
            
    def calculate_output(self, inputs, output_layer=False):
        self.inputs = inputs
        suma = 0
        for i in range(self.num_inputs):
            suma += abs(self.inputs[i] - self.weights[i]) / abs(self.s[i])
        self.output = 1 / (1 + suma)
        return self.output

    
    # The error for each neuron is calculated by the Mean Square Error method:
    def calculate_error(self, target_output):
        return 0.5 * (target_output - self.output) ** 2
 

nn = NeuralNetwork(architecture, dimension)  
best_params = GA_generation(population_size, nn, dimension, mutation_probability, crossover_probability, data, seconds) #, resume = "params_2x8x3.txt")       

nn = NeuralNetwork(architecture, dimension, params = best_params_filename)
print(nn.calculate_total_error(training_sets))

# test on learning set
for i in range(len(training_sets)):
    result = nn.feed_forward(training_sets[i][0])
    numbers = list(result) 
    for j in range(len(result)):
        if result[j] >= 0.5:
            result[j] = 1
        else:
            result[j] = 0
    print(numbers,"\t\t",result,"\t",training_sets[i][1])


