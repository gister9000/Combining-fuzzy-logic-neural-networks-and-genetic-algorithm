from domain import *
from fuzzy_sets import *
from relations import *

# heuristically defined constants used for instantiating fuzzy sets
# used for navigating the ship

# distance categories in pixels        
distance_far = 160
distance_close = 70
distance_critical = 30

# velocity_categories in pixels/second
velocity_fast = 70
velocity_normal = 40
velocity_slow = 10

# how much direction will change in degrees/second
direction_sharp = 10
direction_normal = 6
direction_minimal = 2

# acceleration defines, how much will speed increase in pixels/second
acceleration_big = 11
acceleration_small = 3

# distance domain
distance_domain = simple_domain(0, 1301)
# velocity domain
velocity_domain = simple_domain(0, 501)
# direction domain
direction_domain = simple_domain(-90, 91)
# acceleration domain
acceleration_domain = simple_domain(-35, 36)

# class that contains all possible actions used for navigating  
class action:
        # DISTANCES fuzz
	# returns fuzzy_set which defines distance_far
        def get_distance_far():
                return calculated_fuzzy_set(distance_domain, standard_fuzzy_sets.gamma_function(distance_close, distance_far))
        # returns fuzzy_set which defines distance_close
        def get_distance_close():
                return calculated_fuzzy_set(distance_domain, standard_fuzzy_sets.lambda_function(distance_critical, distance_close, distance_far))
        # returns fuzzy_set which defines distance_critical
        def get_distance_critical():
                return calculated_fuzzy_set(distance_domain, standard_fuzzy_sets.l_function(distance_critical, distance_close))
        
        # VELOCITY fuzz
        # returns fuzzy_set which defines velocity_slow
        def get_velocity_slow():
                return calculated_fuzzy_set(velocity_domain, standard_fuzzy_sets.l_function(velocity_slow, velocity_normal))

        # returns fuzzy_set which defines velocity_normal
        def get_velocity_normal():
                return calculated_fuzzy_set(velocity_domain, standard_fuzzy_sets.lambda_function(velocity_slow, velocity_normal, velocity_fast))

        # returns fuzzy_set which defines velocity_fast
        def get_velocity_fast():
                return calculated_fuzzy_set(velocity_domain, standard_fuzzy_sets.l_function(velocity_normal, velocity_fast))

	# DIRECTION fuzz 
        # options include 3 different turns to each side and straight direction (direction to zero)
        # returns fuzzy_set which defines direction_sharp to the left
        def get_direction_sharp_left():
                return calculated_fuzzy_set(direction_domain, standard_fuzzy_sets.gamma_function(direction_normal, direction_sharp))
        
        # returns fuzzy_set which defines direction_normal to the left
        def get_direction_normal_left():
                return calculated_fuzzy_set(direction_domain, standard_fuzzy_sets.lambda_function(direction_minimal, direction_normal, direction_sharp))
 
        # returns fuzzy_set which defines direction_normal to the left
        def get_direction_minimal_left():
                return calculated_fuzzy_set(direction_domain, standard_fuzzy_sets.lambda_function(0, direction_normal, direction_sharp))  
		
        # returns fuzzy_set which defines direction to be zero
        def get_direction_zero():
                return calculated_fuzzy_set(direction_domain, standard_fuzzy_sets.lambda_function( 0-direction_minimal, 0, direction_minimal))
		
        # returns fuzzy_set which defines direction_sharp to the right
        def get_direction_sharp_right():
                return calculated_fuzzy_set(direction_domain, standard_fuzzy_sets.l_function(0-direction_sharp, 0-direction_normal))
        
        # returns fuzzy_set which defines direction_normal to the right
        def get_direction_normal_right():
                return calculated_fuzzy_set(direction_domain, standard_fuzzy_sets.lambda_function(0-direction_sharp, 0-direction_normal, 0-direction_minimal))
 
        # returns fuzzy_set which defines direction_normal to the right
        def get_direction_minimal_right():
                return calculated_fuzzy_set(direction_domain, standard_fuzzy_sets.lambda_function(0-direction_normal, 0-direction_minimal, 0))  
	
        # ACCELERATION fuzz
        # options include nullifying, small and big acceleration, small and big decceleration
        # returns fuzzy_set which defines zero acceleration
        def get_acceleration_zero():
                return calculated_fuzzy_set(acceleration_domain, standard_fuzzy_sets.lambda_function(0-acceleration_small, 0, acceleration_small))  

        # returns fuzzy_set which defines small decceleration
        def get_decceleration_small():
                return calculated_fuzzy_set(acceleration_domain, standard_fuzzy_sets.lambda_function(0-acceleration_big, 0-acceleration_small, 0))  
	
	# returns fuzzy_set which defines strong decceleration
        def get_decceleration_strong():
                return calculated_fuzzy_set(acceleration_domain, standard_fuzzy_sets.l_function(0-acceleration_big, 0-acceleration_small))  
	
        # returns fuzzy_set which defines small acceleration
        def get_acceleration_small():
                return calculated_fuzzy_set(acceleration_domain, standard_fuzzy_sets.lambda_function(0, acceleration_small, acceleration_big))  
	
	# returns fuzzy_set which defines strong acceleration
        def get_acceleration_strong():
                return calculated_fuzzy_set(acceleration_domain, standard_fuzzy_sets.gamma_function(acceleration_small, acceleration_big))  
	


