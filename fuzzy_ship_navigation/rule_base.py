from domain import *
from fuzzy_sets import *
from relations import *
from fuzzy_rule import *

# collection of rules
class rule_base:
        def __init__(self):
                self.rules = []
                # if LK is very close, slow down a lot and turn sharp right;
                # analogue if DK is very close
                self.rules.append(fuzzy_rule(1, "LK", action.get_direction_sharp_right()))
                self.rules.append(fuzzy_rule(1, "LK", action.get_decceleration_strong()))
                self.rules.append(fuzzy_rule(1, "DK", action.get_direction_sharp_left()))
                self.rules.append(fuzzy_rule(1, "DK", action.get_decceleration_strong()))
                
                # if velocity is slow, accelerate a bit
                self.rules.append(fuzzy_rule("slow", "V", action.get_acceleration_strong()))
                
                # if LK is close, slow down a bit and turn right a bit;
                # analogue if DK is close
                self.rules.append(fuzzy_rule(2, "LK", action.get_direction_normal_right()))
                self.rules.append(fuzzy_rule(2, "LK", action.get_decceleration_small()))
                self.rules.append(fuzzy_rule(2, "DK", action.get_direction_normal_left()))
                self.rules.append(fuzzy_rule(2, "DK", action.get_decceleration_small()))
                
                # if velocity is fast, deccelerate a bit
                self.rules.append(fuzzy_rule("fast", "V", action.get_decceleration_small()))
                
