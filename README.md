# Combining-fuzzy-logic-neural-networks-and-genetic-algorithm
Repo contains implementations of fuzzy logic structures and operations, implementation of neural networks and genetic algorithms. They are first tested separately and then combines in various ways.

# Overview

### Fuzzy stuff
&emsp; fuzzy_sets/<br>
&emsp; fuzzy_relations/<br>
&emsp; fuzzy_ship_navigation/<br>
    
Fuzzy logic data structures and operations are implemented. First practical example is navigating a ship (using fuzzy logic and set of rules) through rivers in simulation (use ship_simulator.jar).
<br> To test the simulator position yourself into fuzzy_ship_navigation folder and run "java -jar ship_simulator.jar".
<br></br>

### Neural stuff
&emsp; neural_network/<br>
Neural network implementation from 0 along with a demo: recognizing humanly written letters. You can use draw.py to generate learning samples. I tested it on writing alfa, beta, gamma, delta and epsilon 20 times each. Works great. <br>
Supports 3 versions of backpropagation learning: online / batches / minibatches. Minibatches seems a little better than the others. <br>
Usage: python3 neural-network.py [batch|online|minibatches] hidden_layer1_num ... output_layer_num <br> 
Keep in mind that output_layer_num must be 5 if you're using my learning data because there are 5 letters. <br></br>

### ANFIS
 &emsp; ANFIS/<br>
An adaptive neuro-fuzzy inference system or adaptive network-based fuzzy inference system (ANFIS) is a kind of artificial neural network that is based on Takagi–Sugeno fuzzy inference system. The technique was developed in the early 1990s. Since it integrates both neural networks and fuzzy logic principles, it has potential to capture the benefits of both in a single framework. Its inference system corresponds to a set of fuzzy IF–THEN rules that have learning capability to approximate nonlinear functions. Hence, ANFIS is considered to be a universal estimator. For using the ANFIS in a more efficient and optimal way, one can use the best parameters obtained by genetic algorithm. It has uses in intelligent situational aware energy management system. <br>
https://en.wikipedia.org/wiki/Adaptive_neuro_fuzzy_inference_system
<br></br>

### Neural network with genetic algorithm for parameter optimization (learning)
&emsp; evolving_NN/<br>
Finally, neural network that finds optimal parameters by mimicking natural selection (genetic algorithm).<br>
Example usage: python3 neurofuzzy.py 2 8 3 <br>
If you use my dataset, make sure last layer has 3 neurons. <br>

	
