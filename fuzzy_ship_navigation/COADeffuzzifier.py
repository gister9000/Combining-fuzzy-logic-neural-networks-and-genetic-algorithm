from domain import *
from fuzzy_sets import *
from relations import *
from fuzzy_rule import *
from rule_base import *
from fuzzy_defines import *
#
# class which defines center average defuzzifier
#
class COADeffuzzifier:
        # empty constructor for now
        def __init__(self):
                pass
        
        #       
        #       function that deffuzzifies
        #       takes fuzzy_set
        #       returns integer
        #
        def deffuzzify(self, fuzz):
                numerator = 0.0
                denominator = 0.0
                for elem in fuzz.domain:
                        numerator += elem.values * fuzz.get_value_at(elem)
                        denominator += fuzz.get_value_at(elem)
                        if denominator == 0.0:
                                denominator = 1.0
                return int(numerator / denominator)
