import sys
from domain import *
from fuzzy_sets import *
from relations import *
from fuzzy_rule import *
from rule_base import *
from fuzzy_defines import *
from COADeffuzzifier import *
from fuzzy_system import *

# brace ourselves
# instantiate center average defuzzifier
deffuzzifier = COADeffuzzifier()  
# instantiate navigation system using COADefuzzyfier
FS_direction = fuzzy_system_direction(deffuzzifier)
# instantiate acceleration systemusing COADefuzzifier
FS_acceleration = fuzzy_system_acceleration(deffuzzifier)

#
#       function that computes new acceleration and direction based on L, D, LK, DK, V, S
#
def fuzzy_magic(L,D,LK,DK,V,S, accel, direct):
        accel = FS_acceleration.execute_rules(L, D, LK, DK, V, S) 
        direct = FS_direction.execute_rules(L, D, LK, DK, V, S)
        # # # # # # # # # # # # # # # #
        return accel, direct

# starting values
acceleration = 5
direction = 0
while True:
        ln_in = input() # read stdin
        L,D,LK,DK,V,S = [int(s) for s in ln_in.split(" ") if s.isdigit()]
        # fuzzy magic
        if ln_in == "KRAJ":
                break
        acceleration, direction = fuzzy_magic(L,D,LK,DK,V,S, acceleration, direction)
        print(str(acceleration) + " " + str(direction))
        sys.stdout.flush()
