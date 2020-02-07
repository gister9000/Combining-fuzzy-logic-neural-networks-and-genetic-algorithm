from domain import *
from fuzzy_sets import *

##################
# LAB 1 DEMO
##################

# domains
print("############ DOMAINS DEMO #############")


d1 = domain.intrange(0,5)
d1.printout("d1:")

d2 = domain.intrange(0,3)
d2.printout("d2:")

d3 = domain.combine(d1,d2)
d3.printout("d3:")

print(d3.element_on_index(0))
print(d3.element_on_index(5))
print(d3.element_on_index(14))
print(d3.index_of_element( (4,1) ) )
print("\n")


d3 = domain.combine(d2,d2,d2)
d3.printout("d3:")


# fuzzy sets
print("############ FUZZY SETS DEMO #############")
d = domain.intrange(0,11)
set1 = mutable_fuzzy_set(d)
set1.set(0,1.0)
set1.set(1,0.8)
set1.set(2,0.6)
set1.set(3,0.4)
set1.set(4,0.2)
set1.set(5,0.0)
set1.printout("Set1:")

d = domain.intrange(-5,6)
set2 = calculated_fuzzy_set(d, standard_fuzzy_sets.lambda_function( d.index_of_element(-4), d.index_of_element(0), d.index_of_element(4) ))
set2.printout("Set2:")

# operations
print("############ OPERATIONS ON FUZZY SETS DEMO #############")
d = domain.intrange(0,11)
set1 = mutable_fuzzy_set(d)
set1.set(0, 1.0)
set1.set(1,0.8)
set1.set(2,0.6)
set1.set(3,0.4)
set1.set(4,0.2)
set1.set(5,0.0)
set1.printout("Set1:")

not_set1 = operations.unary_operation(set1, operations.zadeh_not())
not_set1.printout("Not_Set1:")
union = operations.binary_operation(set1, not_set1, operations.zadeh_or())
union.printout("union:")
hinters = operations.binary_operation(set1, not_set1,  operations.hamacher_Tnorm(1.0))
hinters.printout("hinters")

