from domain import *
#
#       mutable_fuzzy_set contains double type list of values that 
#       correspond to domain_element
#
class mutable_fuzzy_set:
        def __init__(self, domain, values=None):
                self.domain = domain 
                self.memberships = [] #double
                if values:
                        if len(domain.elements) != len(values):
                                raise Exception("Number of values does not match number of domain elems")                         
                        count = 0
                        for item in domain.elements:
                                self.memberships.append(values[count])
                                count += 1
                else:
                        for item in domain.elements:
                                self.memberships.append(0.0)
        
        def get_domain(self):
                return self.domain
                                         
        def get_value_at(self, domain_element):         
                return self.memberships[self.domain.index_of_element(domain_element)]
                        
        def set(self, domain_element_tuple, value):   
                if isinstance(domain_element_tuple, tuple):      
                        self.memberships[self.domain.index_of_element(domain_element.of(domain_element_tuple))] = value   
                else:
                        self.memberships[self.domain.index_of_element( domain_element_tuple)] = value          
        def get_cardinality(self):
                return self.domain.get_cardinality()
                
        def printout(self, heading_text=None):
                print(heading_text)
                count = 0
                for item in self.domain.elements:                
                        print("d(" + str(item) + ")=" + str(self.memberships[count]))
                        count += 1
                print("Cardinality: " + str(self.get_cardinality())+ "\n")
        
#
#       calculated_fuzzy_set contains domain and function f
#       which is used to generate values on the fly
#                        
class calculated_fuzzy_set:
        def __init__(self, domain, f):
                self.domain = domain
                self.f = f #lambda
                
        def get_domain(self):
                return self.domain
                
        def get_value_at(self, i):
                if isinstance(i, domain_element):
                        return self.f(i.values)
                return self.f(self.domain.element_on_index(i).values)
                   
        def get_cardinality(self):
                return self.domain.get_cardinality()
        
        def printout(self, heading_text=None):
                print(heading_text)
                count = 0
                for item in self.domain.elements:                
                        print("d(" + str(item) + ")=" + str(self.f(item.values)) ) 
                        count += 1
                print("Cardinality: " + str(self.get_cardinality())+ "\n")

#
#       standard_fuzzy_sets contains functions
#       for calculated_fuzzy_sets
#
class standard_fuzzy_sets:

        def lambda_function(a, b, c):
                return lambda x : 0 if (x < a) else ( ((float(x) - a) / (b - a)) if ((x >= a) and (x < b)) else ( ((c - float(x)) / (c - b)) if (x >= b and x < c) else 0 ) )
        def gamma_function(a, b):
                return lambda x : 0 if (x < a) else ( 1 if (x >= b) else ((x - a) / (b - a)) )
        def l_function(a, b):
                return lambda x : 1 if (x < a) else ( 0 if (x >= b) else ( (1 - ((x - a) / (b - a))) ) )
                
#
#       operations predefines some operations to be done on fuzzy_sets
#              
class operations:
        # wrapper for unary functions
        def unary_operation(fuzzy_set, unary_function):
                d  = fuzzy_set.get_domain()
                new_set = mutable_fuzzy_set( d )
                for i in range (0, d.get_cardinality()):
                        new_set.set(d.element_on_index(i), unary_function(fuzzy_set.get_value_at(d.element_on_index(i))))
                return new_set
        # wrapper for binary functions
        def binary_operation(fuzzy_set1, fuzzy_set2, binary_function):
                d  = fuzzy_set1.get_domain()
                new_set = mutable_fuzzy_set( d )
                for i in range (0, d.get_cardinality()):
                        new_set.set(d.element_on_index(i), binary_function(fuzzy_set1.get_value_at(d.element_on_index(i)), fuzzy_set2.get_value_at(d.element_on_index(i))))
                return new_set    
        
        def zadeh_not():
                return lambda x : 1 - x
                
        def zadeh_and():
                return lambda x, y : min(x, y)
                
        def zadeh_or():
                return lambda x, y : max(x, y)
                
        def hamacher_Tnorm(z):
                return lambda x, y : (x * y) / (z + (1 - z) * (x + y - x * y))
                
        def hamacher_Snorm(z):
                return lambda x, y : (x + y - (2 - z) * x * y) / (1 - (1 - z) * x * y)
              
