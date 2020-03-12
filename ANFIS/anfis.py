import math
import random
import numpy as np
import matplotlib.pyplot as plt

###     1.1 Priprema podataka za u£enje
lower_limit = -4
upper_limit = 4
def goal_function(x, y):
    return ( (x-1)**2 + (y+2)**2 - 5*x*y + 3 ) * np.cos(x/5)**2

data = []
print("Generating learning data...")
for i in range(-4,5):
    for j in range(-4,5):
        z = goal_function(i,j)
        data.append([i,j,z])
print(data, "\nDone!")


###     1.2 Modeliranje funkcija pripadnosti
def exp_normalize(x):
    b = x.max()
    y = numpy.exp(x - b)
    return y / y.sum()
def sigmoid(x, a, b):
    try:
        return 1 / (1 + np.exp(b * (a - x)))
    except OverflowError:
        return exp_normalize(b * (a - x))

###     1.3 Modeliranje T-norme
def T_norm(ua, ub):
    return ua * ub

###     1.4 Modeliranje z funkcije

def z(x, y, p, q, r):
    return p*x + q*y + r

###     1.5 Modeliranje PI funkcije
def PI(x, y, a, b, c, d):
    return sigmoid(y, a, b) * sigmoid(y, c, d)


###     Klasa ANFIS
class ANFIS:

    def __init__(self, num_rules, learning_rate):
        self.num_rules = num_rules
        self.learning_rate = learning_rate
        self.a = np.random.uniform(-0.5, 0.5, (num_rules, 1))#[ random.uniform(-0.5, 0.5) for i in range(num_rules) ]
        self.b = np.random.uniform(-0.5, 0.5, (num_rules, 1))#[ random.uniform(-0.5, 0.5) for i in range(num_rules) ]
        self.c = np.random.uniform(-0.5, 0.5, (num_rules, 1))#[ random.uniform(-0.5, 0.5) for i in range(num_rules) ]
        self.d = np.random.uniform(-0.5, 0.5, (num_rules, 1))#[ random.uniform(-0.5, 0.5) for i in range(num_rules) ]
        self.p = np.random.uniform(-0.5, 0.5, (num_rules, 1))#[ random.uniform(-0.5, 0.5) for i in range(num_rules) ]
        self.q = np.random.uniform(-0.5, 0.5, (num_rules, 1))#[ random.uniform(-0.5, 0.5) for i in range(num_rules) ]
        self.r = np.random.uniform(-0.5, 0.5, (num_rules, 1))#[ random.uniform(-0.5, 0.5) for i in range(num_rules) ]
        
    # function that returns output for x,y
    # uses preset parameters
    def feed_forward(self, x, y, rule):
        print(self.a[rule])
        layer1_A = sigmoid(x, self.a[rule], self.b[rule])
        layer1_B = sigmoid(y, self.c[rule], self.d[rule])
        layer2 = layer1_A * layer1_B
        layer3 = layer2 / sum(layer2)
        layer4 = layer3 * (self.p[rule]*x + self.q[rule]*y + self.r[rule])
        layer5 = 0
        for i in range(len(layer3)):
            layer5 += layer3[i] * layer4[i]
        return layer5 

    # function that returns error for given learning sample
    def calculate_error(self, x, y, target_output):
        result = self.feed_forward(x, y)
        suma = 0
        for i in range(len(target_output)):
            suma += abs(target_output - result)
        return suma / len(x)

    # function that saves current best params
    def save_params(self):
        with open(str(time.time()), "w") as log:
            for j in range(self.num_rules):
                log.write(self.a[j] + "\n")
                log.write(self.b[j] + "\n")
                log.write(self.c[j] + "\n")
                log.write(self.d[j] + "\n")
                log.write(self.p[j] + "\n")
                log.write(self.q[j] + "\n")
                log.write(self.r[j] + "\n")
                
    # function that performs batch learning algorithm
    def batch_learn(self, data, epsilon, limit):
        count = 0
        while True:
            count += 1
            d_a, d_b, d_c, d_d, d_p, d_q, d_r = [ [0 for j in range(self.num_rules)] for i in range(7)]
            if count > limit:
                self.save_params()
                exit()
            for i in range(len(data)):
                                                  
                x, y, target_output = data[i]
                
                
                suma_brojnik, suma_nazivnik = [0, 0]
                for j in range(self.num_rules): 
                    result = self.feed_forward(x, y, j)
                                                  
                    error = self.calculate_error(x, y, target_output)
                    errors.append(error)

                    if error < epsilon:
                        self.save_params()
                        exit()
                    
                    
                    common = self.learning_rate * (target_output - result) 
                    suma_brojnik += sigmoid(x, self.a[j], self.b[j]) * sigmoid(y, self.c[j], self.d[j]) \
                        * ( z(x, y, self.p[i], self.q[i], self.r[i]) - z(x, y, self.p[j], self.q[j], self.r[j]) )
                    suma_nazivnik += sigmoid(x, self.a[j], self.b[j]) * sigmoid(y, self.c[j], self.d[j])
                    common_razlomak = suma_brojnik / suma_nazivnik**2
                    abcd_same = common * common_razlomak
                    sigmoid_alfa_i = sigmoid(x, self.a[i], self.b[i])
                    sigmoid_beta_i = sigmoid(y, self.c[i], self.d[i])
                    pqr_same = common * sigmoid_alfa_i * sigmoid_beta_i / suma_nazivnik
                                                  
                for j in range(self.num_rules):    
                    d_a[j] += abcd_same * sigmoid_beta_i * self.b[i] * sigmoid_alfa_i * (1 - sigmoid_alfa_i)
                    d_b[j] += abcd_same * sigmoid_beta_i * (self.a[i] - x) * sigmoid_alfa_i * ( 1 - sigmoid_alfa_i)
                    d_c[j] += abcd_same * sigmoid_alfa_i * self.d[i] * sigmoid_beta_i * (1 - sigmoid_beta_i)
                    d_d[j] += abcd_same * sigmoid_alfa_i * (self.c[i] - x) * sigmoid_beta_i * (1 - sigmoid_beta_i)
                    d_p[j] += pqr_same * y
                    d_q[j] += pqr_same * x
                    d_r[j] += pqr_same
            
            for j in range(self.num_rules):
                self.a[j] -= d_a[j]
                self.b[j] -= d_b[j]
                self.c[j] -= d_c[j]
                self.d[j] -= d_d[j]
                self.p[j] -= d_p[j]
                self.q[j] -= d_q[j]
                self.r[j] -= d_r[j]
        # x_draw = np.linspace(-4, 5)
        # y_draw = []
        # for x_d in x_draw:
        #     y_draw.append(sigmoid(x_d, gc[0], gd[0]))
        # plt.plot(x_draw, y_draw)
        # plt.show()
        return errors


    def online_learn(self, data, epsilon, limit):
        count = 0
        errors = []
        while True:
            count += 1
            for i in range(len(data)):
                                                  
                x, y, target_output = data[i]
                                              
                error = self.calculate_error(x, y, target_output)
                errors.append(error)
                suma_brojnik, suma_nazivnik = [0, 0]
                for j in range(self.num_rules): 
                    
                    result = self.feed_forward(x, y, j)


                    common = self.learning_rate * (target_output - result) 
                    suma_brojnik += sigmoid(x, self.a[j], self.b[j]) * sigmoid(y, self.c[j], self.d[j]) \
                        * ( z(x, y, self.p[i], self.q[i], self.r[i]) - z(x, y, self.p[j], self.q[j], self.r[j]) )
                    suma_nazivnik += sigmoid(x, self.a[j], self.b[j]) * sigmoid(y, self.c[j], self.d[j])
                    common_razlomak = suma_brojnik / suma_nazivnik**2
                    abcd_same = common * common_razlomak
                    sigmoid_alfa_i = sigmoid(x, self.a[i], self.b[i])
                    sigmoid_beta_i = sigmoid(y, self.c[i], self.d[i])
                    pqr_same = common * sigmoid_alfa_i * sigmoid_beta_i / suma_nazivnik
                
                # Difference from normal gradient descent
                # Parameters are updated after each sample                                  
                for j in range(self.num_rules):    
                    self.a[j] -= abcd_same * sigmoid_beta_i * self.b[i] * sigmoid_alfa_i * ( 1 - sigmoid_alfa_i )
                    self.b[j] -= abcd_same * sigmoid_beta_i * (self.a[i] - x) * sigmoid_alfa_i * ( 1 - sigmoid_alfa_i )
                    self.c[j] -= abcd_same * sigmoid_alfa_i * self.d[i] * sigmoid_beta_i * (1 - sigmoid_beta_i)
                    self.d[j] -= abcd_same * sigmoid_alfa_i * (self.c[i] - x) * sigmoid_beta_i * (1 - sigmoid_beta_i)
                    self.p[j] -= pqr_same * y
                    self.q[j] -= pqr_same * x
                    self.r[j] -= pqr_same
            
        return errors

#anfis = ANFIS(num_rules=2, learning_rate=0.000001)
#domain = np.linspace(0, 100, 100)

#errors = anfis.batch_learn(data, limit=100, epsilon=0.01)
#plt.plot(domain, errors)

#anfis2 = ANFIS(num_rules=2, learning_rate=0.00005)
#errors2 = anfis.online_learn(data, limit=100, epsilon=0.01)

#plt.plot(domain, errors2)
#plt.show()

#for i in range(len(data)):
#    print(str(data[i][0]),"\t", str(data[i][1]), "\t", ANFIS.feed_forward(data[i][0], data[i][1])[0])

