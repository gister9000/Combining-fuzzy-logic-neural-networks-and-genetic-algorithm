from domain import *
from fuzzy_sets import *
from relations import *
from fuzzy_rule import *
from rule_base import *
from fuzzy_defines import *
from COADeffuzzifier import *

#
# fuzzy system that computes new direction value
#       deffuzzifier defines deffuzzify method to be used     
# 
class fuzzy_system_direction:
        def __init__(self, deffuzzifier):
                self.deffuzzifier = deffuzzifier
                self.rules = []
                # fuzzy_rule knows 1 is critical, 2 is reactable
                rule1 = fuzzy_rule(1, "LK", action.get_direction_sharp_right())
                rule2 = fuzzy_rule(2, "LK", action.get_direction_normal_right())
                rule3 = fuzzy_rule(1, "DK", action.get_direction_sharp_left())
                rule4 = fuzzy_rule(2, "DK", action.get_direction_normal_left())
                self.rules.append(rule1)
                self.rules.append(rule2)
                self.rules.append(rule3)
                self.rules.append(rule4)
                
        def add_rule(rule):
                self.rules.append(rule)
        
        # function that returns new direction value based on simulator data
        def execute_rules(self, L, D, LK, DK, V, S):
                results = []
                for rule in self.rules:
                        results.append(rule.apply(L, D, LK, DK, V, S))
                
                return_set = mutable_fuzzy_set(results[0].domain)
                for fuzz in results:
                        for elem in fuzz.domain:
                                return_set.set(elem, max(return_set.get_value_at(elem), fuzz.get_value_at(elem)))
                                
                return self.deffuzzifier.deffuzzify(return_set)
#
# fuzzy system that computes new acceleration value
#       deffuzzifier defines deffuzzify method to be used     
#                             
class fuzzy_system_acceleration:
        def __init__(self, deffuzzifier):
                self.deffuzzifier = deffuzzifier
                self.rules = []
                # fuzzy_rule knows 1 is critical, 2 is reactable
                rule1 = fuzzy_rule(1, "LK", action.get_decceleration_strong())
                rule2 = fuzzy_rule(1, "DK", action.get_decceleration_strong())
                rule3 = fuzzy_rule(2, "LK", action.get_decceleration_small())
                rule4 = fuzzy_rule(2, "DK", action.get_decceleration_small())
                rule5 = fuzzy_rule("slow", "V", action.get_acceleration_strong())
                rule6 = fuzzy_rule("fast", "V", action.get_decceleration_small())
                self.rules.append(rule1)
                self.rules.append(rule2)
                self.rules.append(rule3)
                self.rules.append(rule4)  
                self.rules.append(rule5)
                self.rules.append(rule6)
                              
        def add_rule(self, rule):
                self.rules.append(rule)

        # function that returns new acceleration value based on simulator data                
        def execute_rules(self, L, D, LK, DK, V, S):
                results = []
                for rule in self.rules:
                        results.append(rule.apply(L, D, LK, DK, V, S))
                
                return_set = mutable_fuzzy_set(results[0].domain)
                for fuzz in results:
                        for elem in fuzz.domain:
                                return_set.set(elem, max(return_set.get_value_at(elem), fuzz.get_value_at(elem)))
                                
                return self.deffuzzifier.deffuzzify(return_set)
