#################################################
# Tuesday July 5 Recitation Starter File
#################################################

#################################################
# Helper functions
#################################################

import math

def almostEqual(d1, d2, epsilon=10**-5): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

######################################################
# sphereVolumeFromSurfaceArea(area)
#
# Write the function sphereVolumeFromSurfaceArea(area) that takes a 
# non-negative number area, and the volume of a sphere with the given 
# surface area. 
######################################################


def testSphereVolumeFromSurfaceArea():
    print("Testing sphereVolumeFromSurfaceArea()...", end="")
    # From http://www.aqua-calc.com/calculate/volume-sphere, with r=3, we see:
    assert(almostEqual(sphereVolumeFromSurfaceArea(452.38934),  904.77868) == True) # r=6
    assert(almostEqual(sphereVolumeFromSurfaceArea(113.09734), 113.09734) == True) # r=3
    assert(almostEqual(sphereVolumeFromSurfaceArea(452.38934),  904) == False) # r=6
    assert(almostEqual(sphereVolumeFromSurfaceArea(452.38934),  905) == False) # r=6
    assert(almostEqual(sphereVolumeFromSurfaceArea(113.09734), 113) == False) # r=3
    assert(almostEqual(sphereVolumeFromSurfaceArea(113.09734), 113.1) == False) # r=3
    print("Passed.")

# testSphereVolumeFromSurfaceArea() # uncomment me to test your answer!

#######################################################
# pittsburghHour
#######################################################

'''
Write the function pittsburghHour(londonHour) that takes a non-negative 
integer, which represents the current hour in London, and returns (as an 
integer) the current hour in Pittsburgh (which is 5 hours behind London). 
However, London time is given in 24-hour time (so londonHour is between 0 and
23, inclusive), but Pittsburgh time must be returned in 12-hour time (so the 
result must be between 1 and 12, inclusive, where "am" and "pm" are ignored). 
'''

# write pittsburghHour here!
def pittsburghHour(londonHour):
    if (londonHour == 5 or londonHour == 17):
        return 12
    return (londonHour + 7) % 12

def testPittsburghHour():
    print('Testing pittsburghHour()... ', end='')
    assert(pittsburghHour(12) == 7)
    assert(pittsburghHour(5) == 12)
    assert(pittsburghHour(17) == 12)
    print('Passed!')

testPittsburghHour() # uncomment to test!

#######################################################
# isAlmostSquare
#######################################################

'''
Write the function isAlmostSquare(n) that takes any Python value and returns 
True if it is an int within 2 (inclusive) of a perfect square, and False 
otherwise. For example, since 25 is a perfect square (5**2), the function 
returns True. The function also returns True if n is 23, 24, 26, or 27, but 
returns False if n is 22 or 28. It also returns False (without crashing) if n is
 25.0 or “25” because these are not ints.
'''

# write isAlmostSquare here!
def isAlmostSquare(n):
    if type(n) != int:
        return False
    for i in range(n-2, n+3):
        if math.sqrt(i) % 1 == 0:
            return True
    return False

#TA METHOD: use roundHalfUp to round the squarerooted decimal and then check if rounded root squared is within two of original number

def testIsAlmostSquare():
    print('Testing isAlmostSquare()... ', end='')
    assert(isAlmostSquare(25) == True)
    assert(isAlmostSquare(23) == True)
    assert(isAlmostSquare(27) == True)
    assert(isAlmostSquare(28) == False)
    assert(isAlmostSquare('25') == False)
    print('Passed!')

testIsAlmostSquare() # uncomment to test!

#######################################################
# Code Tracing 1
#######################################################

def ct1(x):
   print(x)
   x = (x//2*7) + 5
   return x
   print(x+5)

# print(ct1(10)) # uncomment to check answer!

#######################################################
# Code Tracing 2
#######################################################
def ct2(x, y, z): 
    print(x/y + x//y + int(x/y)) 
    print(y**z + y%z) 
    a = int(x) / int(y)
    return isinstance(a, int) 

# print(ct2(6, 4, 3)) # uncomment to check answer!

# Attendance Link: https://tinyurl.com/reccy1