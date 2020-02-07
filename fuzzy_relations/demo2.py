from domain import *
from fuzzy_sets import *
from relations import *

##################
# LAB  2 DEMO
##################

# osnovna svojstva neizrazite relacije
u = domain.intrange(1,6);
u2 = domain.combine(u, u)
r1 = mutable_fuzzy_set(u2)
r1.set( (1,1), 1.0 )
r1.set( (2,2), 1.0 )
r1.set( (3,3), 1.0 )
r1.set( (4,4), 1.0 )
r1.set( (5,5), 1.0 )
r1.set( (3,1), 0.5 )
r1.set( (1,3), 0.5 )
r2 = mutable_fuzzy_set(u2)
r2.set( (1,1), 1.0 )
r2.set( (2,2), 1.0 )
r2.set( (3,3), 1.0 )
r2.set( (4,4), 1.0 )
r2.set( (5,5), 1.0 )
r2.set( (3,1), 0.5 )
r2.set( (1,3), 1.0 )
r3 = mutable_fuzzy_set(u2)
r3.set( (1,1), 1.0 )
r3.set( (2,2), 1.0 )
r3.set( (3,3), 0.3 )
r3.set( (4,4), 1.0 )
r3.set( (5,5), 1.0 )
r3.set( (1,2), 0.6 )
r3.set( (2,1), 0.6 )
r3.set( (2,3), 0.7 )
r3.set( (3,2), 0.7 )
r3.set( (3,1), 0.5 )
r3.set( (1,3), 0.5 )
r4 = mutable_fuzzy_set(u2)
r4.set( (1,1), 1.0 )
r4.set( (2,2), 1.0 )
r4.set( (3,3), 1.0 )
r4.set( (4,4), 1.0 )
r4.set( (5,5), 1.0 )
r4.set( (1,2), 0.4 )
r4.set( (2,1), 0.4 )
r4.set( (2,3), 0.5 )
r4.set( (3,2), 0.5 )
r4.set( (1,3), 0.4 )
r4.set( (3,1), 0.4 )

test1 = relation.isUtimesUrelation(r1)
print("r1 je definiran nad UxU? "+ str(test1))
test2 = relation.isSymmetric(r1)
print("r1 je simetricna? "+str(test2))
test3 = relation.isSymmetric(r2)
print("r2 je simetricna? "+str(test3))
test4 = relation.isReflexive(r1)
print("r1 je refleksivna? "+str(test4))
test5 = relation.isReflexive(r3)
print("r3 je refleksivna? "+str(test5))
test6 = relation.isMaxMinTransitive(r3)
print("r3 je max-min tranzitivna? "+str(test6))
test7 = relation.isMaxMinTransitive(r4)
print("r4 je max-min tranzitivna? "+str(test7))

# kompozicija neizrazite relacije
u1 = domain.intrange(1,5)
u2 = domain.intrange(1,4)
u3 = domain.intrange(1,5)

r1 = mutable_fuzzy_set(domain.combine(u1,u2))
r1.set(domain_element.of((1,1)), 0.3)
r1.set(domain_element.of((1,2)), 1.0)
r1.set(domain_element.of((3,3)), 0.5)
r1.set(domain_element.of((4,3)), 0.5)

r2 = mutable_fuzzy_set(domain.combine(u2,u3))
r2.set(domain_element.of((1,1)), 1.0)
r2.set(domain_element.of((2,1)), 0.5)
r2.set(domain_element.of((2,2)), 0.7)
r2.set(domain_element.of((3,3)), 1.0)
r2.set(domain_element.of((3,4)), 0.4)
r1.printout("")
r2.printout("")
r1r2 = relation.compose_binary_relations(r1,r2)

for element in r1r2.domain:
        print("mu(" + str(element) + ")=" + str(r1r2.get_value_at(element)))
        
# fuzzy equivalence
u = domain.intrange(1,5)
r = mutable_fuzzy_set(domain.combine(u,u))
r.set(domain_element.of((1,1)), 1.0)
r.set(domain_element.of((2,2)), 1.0)
r.set(domain_element.of((3,3)), 1.0)
r.set(domain_element.of((4,4)), 1.0)
r.set(domain_element.of((1,2)), 0.3)
r.set(domain_element.of((2,1)), 0.3)
r.set(domain_element.of((2,3)), 0.5)
r.set(domain_element.of((3,2)), 0.5)
r.set(domain_element.of((3,4)), 0.2)
r.set(domain_element.of((4,3)), 0.2)

r2 = mutable_fuzzy_set(domain.combine(u,u))
r2.set(domain_element.of((1,1)), 1.0)
r2.set(domain_element.of((2,2)), 1.0)
r2.set(domain_element.of((3,3)), 1.0)
r2.set(domain_element.of((4,4)), 1.0)
r2.set(domain_element.of((1,2)), 0.3)
r2.set(domain_element.of((2,1)), 0.3)
r2.set(domain_element.of((2,3)), 0.5)
r2.set(domain_element.of((3,2)), 0.5)
r2.set(domain_element.of((3,4)), 0.2)
r2.set(domain_element.of((4,3)), 0.2)

print("Pocetna relacija je neizrazita relacija ekvivalencije?", end="")
print(relation.isFuzzyEquivalence(r2))

for i in range(1, 4):
        r2 = relation.compose_binary_relations(r2, r)
        print("Broj odradenih kompozicija: " + str(i) + ". Relacija je:")
        for elem in r2.domain:
                print("mu(" + str(elem) + ")=" + str(r2.get_value_at(elem)))
        print("Ova relacija je neizrazita relacija ekvivalencije? ", end ="")
        print(relation.isFuzzyEquivalence(r2))
        
