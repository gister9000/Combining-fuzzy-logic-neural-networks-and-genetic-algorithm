from domain import *
from fuzzy_sets import *

# helper function for other functions
def isUtimesUdomain(r):
        return relation.isUtimesUrelation(r)

class relation:
        # checks wheter relation is defined under UxU domain
        def isUtimesUrelation(relation):
        
                first = relation.domain.element_on_index(0)
                last = relation.domain.element_on_index(relation.domain.kard - 1)
                return first.get_component_value(0).values == first.get_component_value(1).values and last.get_component_value(0).values == last.get_component_value(1).values
               
        # checks wheter relation is defined under symmetric UxU domain
        def isSymmetric(relation):
                if not isUtimesUdomain(relation):
                        print("relation has to be UxU to be symmetric")
                        return False
                symmetric = True
                for element in relation.domain:
                        if relation.get_value_at(element) != relation.get_value_at(domain_element.of( (element.get_component_value(1).values, element.get_component_value(0).values) )):
                                symmetric = False
                                break
                return symmetric
                
        # checks if given relation is under reflexive UxU domain
        def isReflexive(relation):
                if not isUtimesUdomain(relation):
                        print("relation has to be UxU to be symmetric")
                        return False
                reflexive = True
                for element in relation.domain:
                        if element.get_component_value(0) == element.get_component_value(1) and relation.get_value_at(element) != 1:
                                reflexive = False
                return reflexive
        
        # checks if given relation is under MinMax transitive UxU domain        
        def isMaxMinTransitive(relation):
                if not isUtimesUdomain(relation):
                        print("relation has to be UxU to be symmetric")
                        return False
                transitive = True
                
                for i in range(0, relation.domain.kard):
                        for j in range(0, relation.domain.kard):
                                if relation.domain.element_on_index(i).get_component_value(1) == relation.domain.element_on_index(j).get_component_value(0):
                                        element = domain_element.of( (relation.domain.element_on_index(i).get_component_value(0), relation.domain.element_on_index(j).get_component_value(1)))
                                        if relation.get_value_at(element) < min(relation.get_value_at(relation.domain.element_on_index(i)), relation.get_value_at(relation.domain.element_on_index(j))):
                                                transitive = False
                return transitive
                
        # combines two fuzzy relations into a composition
        # returns the new relation as a fuzzy_set
        def compose_binary_relations(r1, r2):
                
                X_start = r1.domain.elements[0].values[0].values
                X_end = r1.domain.elements[ r1.domain.kard - 1 ].values[0].values
                Y_start = r2.domain.elements[0].values[1].values
                Y_end = r2.domain.elements[ r2.domain.kard - 1 ].values[1].values
                
                r1_cols = r1.domain.elements[ r1.domain.kard - 1 ].values[1].values - r1.domain.elements[0].values[1].values
                r2_rows = r2.domain.elements[ r2.domain.kard - 1 ].values[0].values - r2.domain.elements[0].values[0].values
                
                if  r1_cols != r2_rows:
                        raise Exception("relations cannot be composed")
                
                composition_domain = domain.combine( domain.intrange(X_start, X_end+1), domain.intrange( Y_start, Y_end+1 ) )
                #composition_domain.printout("composed domain debug check")
                
                relation = mutable_fuzzy_set(composition_domain)
                for item in composition_domain:
                        x = item.values[0]
                        y = item.values[1]
                        mins = []
                        for i in range(r1.domain.elements[0].values[1].values, r1.domain.elements[r1.domain.kard - 1].values[1].values + 1):
                                mins.append( min(r1.get_value_at(domain_element.of((x,i))), r2.get_value_at(domain_element.of((i,y))) ) )
                        #print(mins)
                        relation.set(item, max(mins) )

                return relation
        
        # checks if relation is reflexive, symmetric and max-min transitive
        def isFuzzyEquivalence(r):
                return relation.isReflexive(r) and relation.isSymmetric(r) and relation.isMaxMinTransitive(r)
