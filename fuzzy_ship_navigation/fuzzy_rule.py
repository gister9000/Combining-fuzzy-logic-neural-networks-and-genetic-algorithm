from domain import *
from fuzzy_sets import *
from relations import *
from fuzzy_defines import *

#
#       class which defines fuzzy rule for controlling simulated boat
#
class fuzzy_rule:
       #
       #        fuzzy_rule constructor; accepts:
       #                condition - integer for proximity (1 is critically close), "slow" or "fast" for velocity
       #                param - variable related to the condition
       #                fuzz - fuzzy set to be modified
       #
       def __init__(self, condition, param, fuzz):
                self.condition = condition
                self.param = param
                self.fuzz = fuzz
       
       # function that applies the rule
       # takes simulators data L, D, LK, DK, V, S integers
       # returns a fuzzy_set 
       def apply(self, L, D, LK, DK, V, S):
                variables_dict = { "L": L, "D": D, "LK": LK, "DK": DK, "V": V, "S": S, }
                # transform condition variable to fuzzy set 
                if self.condition == 1:
                        condition_set = action.get_distance_critical()
                elif self.condition == 2:
                        condition_set = action.get_distance_close()
                elif self.condition == 3:
                        condition_set = action.get_distance_far()
                elif self.condition == "slow":
                        condition_set = action.get_velocity_slow()
                elif self.condition == "normal":
                        condition_set = action.get_velocity_normal()
                elif self.condition == "fast":
                        condition_set = action.get_velocity_fast()
                else:
                        raise Exception("invalid condition")
                
                # double which represents membership factor
                affiliation = condition_set.get_value_at(domain_element.of(variables_dict[self.param]))
                # fuzzy set which will be returned after setting the values
                return_set = mutable_fuzzy_set(self.fuzz.domain)
                for elem in self.fuzz.domain:
                        return_set.set(elem, affiliation * self.fuzz.get_value_at(elem))
                return return_set
