# Combining-fuzzy-logic-neural-networks-and-genetic-algorithm
Repo contains implementations of fuzzy logic structures and operations, implementation of neural networks and genetic algorithms. They are first tested separately and then combines in various ways.

# Overview
Fuzzy logic data structures and operations are implemented in:
    fuzzy_sets/
    fuzzy_relations/
First practical example is navigating a ship (using fuzzy logic and set of rules) through rivers in simulation (need to include the simulation .jar file to be testable #TODO)
    fuzzy_ship_navigation/
<br>
Neural network implementation from 0 along with a demo: recognizing humanly written letters. You can use draw.py to generate learning samples. I tested it on writing alfa, beta, gamma, delta and epsilon 20 times each. Works great. 
    neural_network/
<br>
An adaptive neuro-fuzzy inference system or adaptive network-based fuzzy inference system (ANFIS) is a kind of artificial neural network that is based on Takagi–Sugeno fuzzy inference system. The technique was developed in the early 1990s. Since it integrates both neural networks and fuzzy logic principles, it has potential to capture the benefits of both in a single framework. Its inference system corresponds to a set of fuzzy IF–THEN rules that have learning capability to approximate nonlinear functions.[3] Hence, ANFIS is considered to be a universal estimator. For using the ANFIS in a more efficient and optimal way, one can use the best parameters obtained by genetic algorithm. It has uses in intelligent situational aware energy management system.
    ANFIS/
<br>
Finally, neural network that finds optimal parameters by mimicking natural selection (genetic algorithm).
	evolving_NN/
	
