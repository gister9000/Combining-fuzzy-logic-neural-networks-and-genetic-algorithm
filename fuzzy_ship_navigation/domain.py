import itertools
#
#       helper class used to instantiate domains easily
#
class domain:
        def intrange(start, end):
                return simple_domain(start,end)
                
        def combine(*domain):
                return composite_domain(*domain)
#
#       domain_element represented as n-tuple or int
#
class domain_element:
        #
        #       constructor
        #       creates:
        #               int from int
        #               tuple from tuple, list or other
        #
        def __init__(self, values):
                if isinstance(values, int):
                        self.values = values
                elif isinstance(values, tuple):
                        self.values = values
                else:
                        try:
                                self.values = tuple(values)
                        except TypeError:
                                self.values = values.values
                                
        def get_number_of_components(self):
                return len(self.values)
                
        def get_component_value(self, i):
                return self.values[i]
  
        def __eq__(self, obj):                         
                if isinstance(self.values, int) and isinstance(obj, int):
                        return self.values == obj     
                
                t1 = self.values
                t2 = obj
                if isinstance(obj, domain_element):
                        t2 = obj.values
                try:
                        if len(t1) != len(t2):
                                return False   
                except TypeError:
                        return self.values == obj
                equal = True
                for i in range(0, len(t1)):
                        if t1[i] != t2[i]:
                                equal = False
                return equal
                        
        def __repr__(self):
                return str(self.values)
        
        def of(values):
                return domain_element(values)
#
#       simple_domain reoresents domain in which start and end
#       element define it's boundaries
#
class simple_domain:
        #
        #       constructor
        #       creates:
        #               list of domain_element elements
        #               
        #       start - begining of the range
        #       end - end of the range
        #
        def __init__ (self, start, end):
                self.iterator = 0
                self.first = start # int
                self.last = end    # int
                self.elements = [] # filled with domain_element
                for i in range(self.first, self.last):
                        self.elements.append(domain_element(i))
                self.kard = len(self.elements)                 
                
        def printout(self, heading_text=None):
                print(heading_text)
                print("Domain elements:")
                for item in self.elements:
                        print("Domain element: " + str(item))
                print("Cardinality: " + str(self.kard) + "\n")
        
        def get_cardinality(self):
                return self.kard               
        
        def element_on_index(self, index):
                return self.elements[index]
        
        def index_of_element(self, elem):
                if isinstance(elem, domain_element):
                        return self.elements.index(elem)
                else:
                        return self.elements.index(domain_element.of(elem))     
                           
        def __iter__(self):
                return self

        def __next__(self):
                if self.iterator >= self.kard:
                        self.iterator = 0
                        raise StopIteration
                else:
                        self.iterator += 1
                        return self.elements[self.iterator - 1]

        
#        
#      composite_domain represents cartesian product
#       of 2 simple_domain
#
class composite_domain:
        #
        #       constructor
        #       creates:
        #               list of domain_element elements by doing 
        #               cartesian product of arbitrary number
        #               of domains
        #
        def __init__ (self, *domains):
                self.iterator = 0
             
                temporary_domain = list(itertools.product(*domains))
                
                self.elements = []
                for item in temporary_domain:
                        self.elements.append(domain_element(item))
                self.kard = len(self.elements)
                self.first = self.elements[0]
                self.last = self.elements[len(self.elements)-1]
       
        def printout(self, heading_text=None):
                print(heading_text)
                print("Domain elements:")
                for item in self.elements:                        
                        print("Domain element: " + str(item))        
                print("Cardinality: " + str(self.kard) + "\n")
                      
        def get_cardinality(self):
                return self.kard               
        
        def element_on_index(self, index):
                return self.elements[index]
        
        def index_of_element(self, elem):
                if isinstance(elem, domain_element):
                        #if elem == (1,1):       input(self.elements)
                        return self.elements.index(elem)
                else:
                        return self.elements.index(domain_element.of(elem))   
                
                            
        def __iter__(self):
                return self

        def __next__(self):
                if self.iterator >= self.kard:
                        self.iterator = 0
                        raise StopIteration
                else:
                        self.iterator += 1
                        return self.elements[self.iterator - 1]


