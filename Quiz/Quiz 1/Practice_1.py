#################################################
# Basic Problem Set #1
# Data Types, Functions, Operations, and Conditionals
#################################################

# Many of these problems come directly from
# the course notes. So, try to complete them without
# looking at the notes! Then, if there are
# problems that you couldn't figure out,
# take another look at the course notes!

#################################################
# Helper functions
#################################################

import decimal
import math


def almostEqual(d1, d2, epsilon=10**-2):  # helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)


def roundHalfUp(d):  # helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#####################################################
# add(a, b)
#####################################################

# Write the function add(a, b), that takes in two integers,
# a and b, and returns the value a + b

# Note: would there be a difference if we did a + b or b + a?

# write add here!


def add(a, b):
    return a + b


def testAdd():
    print('Testing add()...', end='')
    assert(add(3, 4) == 7)
    assert(add(0, 5) == 5)
    assert(add(-3, 5) == 2)
    assert(add(-6, -6) == -12)
    print('Passed!')


testAdd()  # uncomment to test

#####################################################
# subtract(a, b)
#####################################################

# Write the function subtract(a, b), that takes in two integers,
# a and b, and returns the value a - b

# Note: would there be a difference if we did a - b or b - a?

# write subtract here!


def subtract(a, b):
    return a - b


def testSubtract():
    print('Testing subtract()...', end='')
    assert(subtract(7, 3) == 4)
    assert(subtract(9, 4) == 5)
    assert(subtract(4, -4) == 8)
    assert(subtract(-8, -8) == 0)
    print('Passed!')


testSubtract()  # uncomment to test

#####################################################
# power(a, b)
#####################################################

# Write the function power(a, b), that takes in two integers,
# a and b, and returns the value a^b (a to the power of b).
# b is guaranteed to be a non-negative integer

# write power here!


def power(a, b):
    return a ** b


def testPower():
    print('Testing power()...', end='')
    assert(power(2, 3) == 8)
    assert(power(4, 2) == 16)
    assert(power(-3, 3) == -27)
    assert(power(100, 0) == 1)
    print('Passed!')


testPower()  # uncomment to test

#####################################################
# mod(a, b)
#####################################################

# Write the function mod(a, b), that takes in two integers,
# a and b, and returns the value a % b.
# However, try not to use the % operator in your solution.

# Before writing any code, try and think about
# how mod can be represented using a mathematical formula.
# Once you have a good idea of how to write mod using math,
# it should be easier to write the function!

# write mod here!


def mod(a, b):
    return roundHalfUp((a / b - a // b) * b)


def testMod():
    print('Testing mod()...', end='')
    assert(mod(4, 3) == 1)
    assert(mod(3, 3) == 0)
    assert(mod(1, 2) == 1)
    assert(mod(24, 5) == 4)
    print('Passed!')


testMod()  # uncomment to test

# ###################################################
# isEvenInt(x)
# ###################################################

# Write the function isEvenInt(x), which determines
# whether x is an even integer
# Return True if x is an even integer and False if x is not an even integer

# write isEvenInt here!


def isEvenInt(x):
    if not isinstance(x, int):
        return False
    return x % 2 == 0


def testIsEvenInt():
    print('Testing isEvenInt()... ', end='')
    assert(isEvenInt(2) == True)
    assert(isEvenInt(3) == False)
    assert(isEvenInt(0) == True)
    assert(isEvenInt(4.3) == False)
    assert(isEvenInt('Chee') == False)
    print('Passed!')

# testIsEvenInt() # uncomment to test!

#######################################################
# isOddInt(x)
#######################################################

# Write the function isOddInt(x), which determines whether
# x is an odd integer
# Return True if x is an odd integer and False if x is not an odd integer

# write isOddInt here!


def isOddInt(x):
    if not isinstance(x, int):
        return False
    return not isEvenInt(x)


def testIsOddInt():
    print('Testing isOddInt()... ', end='')
    assert(isOddInt(2) == False)
    assert(isOddInt(3) == True)
    assert(isOddInt(0) == False)
    assert(isOddInt(-3.3) == False)
    assert(isOddInt('Three') == False)
    print('Passed!')


testIsOddInt()  # uncomment to test!

#######################################################
# onesDigit(n)
#######################################################

# Write the function onesDigit(n), which returns the ones
# digit of the non-negative integer n.
# Which operator did we learn about
# that can help us isolate the ones digit of a number?
# Do you know why it works? If not, ask a TA!

# write onesDigit here!


def onesDigit(n):
    return n % 10


def testOnesDigit():
    print('Testing onesDigit()... ', end='')
    assert(onesDigit(25) == 5)
    assert(onesDigit(23) == 3)
    assert(onesDigit(27) == 7)
    assert(onesDigit(28) == 8)
    print('Passed!')


testOnesDigit()  # uncomment to check

#######################################################
# newCircleArea(a, b)
#######################################################

# Two circles exist with radii of a and b, where a and b are integers.
# Imagine these circles are placed next to each other so that they touching
# at exactly one point and a new circle is drawn around them such that
# the new circle's diameter is equal to the sum of the two circle's diameters.
# What is the area of this new circle?

# Hint: Draw a picture to help visualize this problem!

# write newCircleArea(a, b) here!


def newCircleArea(a, b):
    return (a + b) ** 2 * math.pi


def testNewCircleArea():
    print('Testing newCircleArea()... ', end='')
    assert(almostEqual(newCircleArea(10, 3), 530.93))
    assert(almostEqual(newCircleArea(3, 2), 78.54))
    assert(almostEqual(newCircleArea(4, 4), 201.06))
    print('Passed!')


testNewCircleArea()  # uncomment to test!

#######################################################
# ferrisWheelRotations(stops)
#######################################################

# You are sitting on a ferris wheel that stops 16 times
# during each rotation so that everybody can get a good
# view from the top. You have counted that the ferris wheel
# has stopped a total of 'stops' times since you got on.
# How many full rotations have you made around the ferris wheel?

# write ferrisWheelRotations here!


def ferrisWheelRotations(stops):
    return stops // 16


def testFerrisWheelRotations():
    print('Testing ferrisWheelRotations()... ', end='')
    assert(ferrisWheelRotations(72) == 4)
    assert(ferrisWheelRotations(32) == 2)
    assert(ferrisWheelRotations(3) == 0)
    print('Passed!')


testFerrisWheelRotations()  # uncomment to test!

#######################################################
# ferrisWheelStopsLeft(stops)
#######################################################

# You are sitting on a ferris wheel that stops 16 times
# during each rotation so that everybody can get a good
# view from the top. You have counted that the ferris wheel
# has stopped a total of 'stops' times since you got on.
# The ride operator has alerted you that this is your last
# rotation before the ride ends. How many more stops do you have?

# write ferrisWheelStopsLeft here!


def ferrisWheelStopsLeft(stops):
    return 16 - stops % 16


def testFerrisWheelStopsLeft():
    print('Testing ferrisWheelStopsLeft()... ', end='')
    assert(ferrisWheelStopsLeft(72) == 8)
    assert(ferrisWheelStopsLeft(32) == 16)
    assert(ferrisWheelStopsLeft(3) == 13)
    assert(ferrisWheelStopsLeft(63) == 1)
    print('Passed!')


testFerrisWheelStopsLeft()  # uncomment to test!

#####################################################
# getGrade(score)
#####################################################

# At CMU, we use the following score cutoffs:
# >= 90 is an A
# >= 80 is a B
# >= 70 is a C
# >= 60 is a D
# < 60 is an R

# Write the function getGrade(score), which takes in an integer
# score on an arbitrary test and returns the grade that a student
# will get, as a string. A string can be formed by surrounding a
# character or string of characters with two apostrophes or two
# quotation marks, as such: "This is a string", 'This is also a string'.
# So, to return a grade of A as a string, you can return "A" or 'A'.
# Return None if the input is not an integer.

# write getGrade here!


def getGrade(score):
    if not isinstance(score, int):
        return None
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'R'


def testGetGrade():
    print('Testing getGrade()...', end='')
    assert(getGrade(83) == "B")
    assert(getGrade(97) == "A")
    assert(getGrade(42) == "R")
    assert(getGrade("0") == None)
    print('Passed!')


testGetGrade()  # uncomment to test
