#################################################
# hw1.py
# name:
# andrew id:
#################################################

import cs112_n22_week1_hw1_linter
import math

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# hw1-standard-functions
#################################################

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def circlesIntersect(x1, y1, r1, x2, y2, r2):
    d = distance(x1, y1, x2, y2)
    return d <= r1 + r2

def getKthDigit(n, k):
    return abs(n) // (10 ** k) % 10

def setKthDigit(n, k, d):
    if n < 0:
        return n + getKthDigit(n, k) * (10 ** k) - d * (10 ** k)
    else:
        return n - getKthDigit(n, k) * (10 ** k) + d * (10 ** k)

def fabricYards(inches):
    if inches % 36 == 0:
        return inches // 36
    return inches // 36 + 1
 
def fabricExcess(inches):
    return fabricYards(inches) * 36 - inches


#################################################
# hw1-bonus-functions
# these are optional! You may (and should) write 
# and use additional helper functions!
#################################################

def lineIntersectX(m1, b1, m2, b2): #helper-fn
    return (b2 - b1) / (m1 - m2)
def lineIntersectY(m1, b1, m2, b2):
    return m1 * lineIntersectX(m1, b1, m2, b2) + b1

def threeLinesArea(m1, b1, m2, b2, m3, b3):
    if m1 == m2 or m2 == m3 or m3 == m1:
        return 0 #no triangle formed

    x1 = lineIntersectX(m1, b1, m2, b2)
    y1 = lineIntersectY(m1, b1, m2, b2)

    x2 = lineIntersectX(m2, b2, m3, b3)
    y2 = lineIntersectY(m2, b2, m3, b3)

    x3 = lineIntersectX(m3, b3, m1, b1)
    y3 = lineIntersectY(m3, b3, m1, b1)

    s1 = distance(x1, y1, x2, y2)
    s2 = distance(x2, y2, x3, y3)
    s3 = distance(x3, y3, x1, y1)

    s = (s1 + s2 + s3) / 2

    #heron's formula
    return math.sqrt(s * (s - s1) * (s - s2) * (s - s3))

def colorBlender(rgb1, rgb2, midpoints, n):
    if n < 0 or n > midpoints + 1:
        return None
    r1 = rgb1 // 1000000
    g1 = rgb1 // 1000 % 1000
    b1 = rgb1 % 1000
    r2 = rgb2 // 1000000
    g2 = rgb2 // 1000 % 1000
    b2 = rgb2 % 1000

    r = roundHalfUp(r1 + (r2 - r1) / (midpoints + 1) * n)
    g = roundHalfUp(g1 + (g2 - g1) / (midpoints + 1) * n)
    b = roundHalfUp(b1 + (b2 - b1) / (midpoints + 1) * n)
    
    return r * 1000000 + g * 1000 + b

def findIntRootsOfCubic(a, b, c, d):
    # you are assured a != 0
    # you are also assured the answer will be 3 integers!
    return 42

#################################################
# Test Functions
#################################################

def myTest(): #temp func for own test
    colorBlender(220020060, 189252201, 3, 1) 
def testDistance():
    print('Testing distance()... ', end='')
    assert(almostEqual(distance(0, 0, 3, 4), 5))
    assert(almostEqual(distance(-1, -2, 3, 1), 5))
    assert(almostEqual(distance(-.5, .5, .5, -.5), 2**0.5))
    print('Passed!')

def testCirclesIntersect():
    print('Testing circlesIntersect()... ', end='')
    assert(circlesIntersect(0, 0, 2, 3, 0, 2) == True)
    assert(circlesIntersect(0, 0, 2, 4, 0, 2) == True)
    assert(circlesIntersect(0, 0, 2, 5, 0, 2) == False)
    assert(circlesIntersect(3, 3, 3, 3, -3, 3) == True)
    assert(circlesIntersect(3, 3, 3, 3,- 3, 2.99) == False)
    print('Passed!')

def testGetKthDigit():
    print('Testing getKthDigit()... ', end='')
    assert(getKthDigit(809, 0) == 9)
    assert(getKthDigit(809, 1) == 0)
    assert(getKthDigit(809, 2) == 8)
    assert(getKthDigit(809, 3) == 0)
    assert(getKthDigit(0, 100) == 0)
    assert(getKthDigit(-809, 0) == 9)
    print('Passed.')

def testSetKthDigit():
    print('Testing setKthDigit()... ', end='')
    assert(setKthDigit(809, 0, 7) == 807)
    assert(setKthDigit(809, 1, 7) == 879)
    assert(setKthDigit(809, 2, 7) == 709)
    assert(setKthDigit(809, 3, 7) == 7809)
    assert(setKthDigit(0, 4, 7) == 70000)
    assert(setKthDigit(-809, 0, 7) == -807)
    print('Passed.')

def testFabricYards():
    print('Testing fabricYards()... ', end='')
    assert(fabricYards(0) == 0)
    assert(fabricYards(1) == 1)
    assert(fabricYards(35) == 1)
    assert(fabricYards(36) == 1)
    assert(fabricYards(37) == 2)
    assert(fabricYards(72) == 2)
    assert(fabricYards(73) == 3)
    assert(fabricYards(108) == 3)
    assert(fabricYards(109) == 4)
    print('Passed.')
 
def testFabricExcess():
    print('Testing fabricExcess()... ', end='')
    assert(fabricExcess(0) == 0)
    assert(fabricExcess(1) == 35)
    assert(fabricExcess(35) == 1)
    assert(fabricExcess(36) == 0)
    assert(fabricExcess(37) == 35)
    assert(fabricExcess(72) == 0)
    assert(fabricExcess(73) == 35)
    assert(fabricExcess(108) == 0)
    assert(fabricExcess(109) == 35)
    print('Passed.')



def testThreeLinesArea():
    print('Testing threeLinesArea()... ', end='')
    assert(almostEqual(threeLinesArea(1, 2, 3, 4, 5, 6), 0))
    assert(almostEqual(threeLinesArea(0, 7, 1, 0, -1, 2), 36))
    assert(almostEqual(threeLinesArea(0, 3, -.5, -5, 1, 3), 42.66666666666666))
    assert(almostEqual(threeLinesArea(1, -5, 0, -2, 2, 2), 25))
    assert(almostEqual(threeLinesArea(0, -9.75, -6, 2.25, 1, -4.75), 21))
    assert(almostEqual(threeLinesArea(1, -5, 0, -2, 2, 25), 272.25))
    print('Passed.')

def testColorBlender():
    print('Testing colorBlender()... ', end='')
    # http://meyerweb.com/eric/tools/color-blend/#DC143C:BDFCC9:3:rgbd
    assert(colorBlender(220020060, 189252201, 3, -1) == None)
    assert(colorBlender(220020060, 189252201, 3, 0) == 220020060)
    assert(colorBlender(220020060, 189252201, 3, 1) == 212078095)
    assert(colorBlender(220020060, 189252201, 3, 2) == 205136131)
    assert(colorBlender(220020060, 189252201, 3, 3) == 197194166)
    assert(colorBlender(220020060, 189252201, 3, 4) == 189252201)
    assert(colorBlender(220020060, 189252201, 3, 5) == None)
    # http://meyerweb.com/eric/tools/color-blend/#0100FF:FF0280:2:rgbd
    assert(colorBlender(1000255, 255002128, 2, -1) == None)
    assert(colorBlender(1000255, 255002128, 2, 0) == 1000255)
    assert(colorBlender(1000255, 255002128, 2, 1) == 86001213)
    assert(colorBlender(1000255, 255002128, 2, 2) == 170001170)
    assert(colorBlender(1000255, 255002128, 2, 3) == 255002128)
    print('Passed.')

def getCubicCoeffs(k, root1, root2, root3): #helper-fn
    # helper function for testFindIntRootsOfCubic
    # Given roots e,f,g and vertical scale k, we can find
    # the coefficients a,b,c,d as such:
    # k(x-e)(x-f)(x-g) =
    # k(x-e)(x^2 - (f+g)x + fg)
    # kx^3 - k(e+f+g)x^2 + k(ef+fg+eg)x - kefg
    e,f,g = root1, root2, root3
    return k, -k*(e+f+g), k*(e*f+f*g+e*g), -k*e*f*g

def testFindIntRootsOfCubicCase(k, z1, z2, z3): #helper-fn
    # helper function for testFindIntRootsOfCubic
    a,b,c,d = getCubicCoeffs(k, z1, z2, z3)
    result1, result2, result3 = findIntRootsOfCubic(a,b,c,d)
    m1 = min(z1, z2, z3)
    m3 = max(z1, z2, z3)
    m2 = (z1+z2+z3)-(m1+m3)
    actual = (m1, m2, m3)
    assert(almostEqual(m1, result1))
    assert(almostEqual(m2, result2))
    assert(almostEqual(m3, result3))

def testFindIntRootsOfCubic():
    print('Testing findIntRootsOfCubic()...', end='')
    testFindIntRootsOfCubicCase(5, 1, 3,  2) #helper-fn
    testFindIntRootsOfCubicCase(2, 5, 33, 7) #helper-fn
    testFindIntRootsOfCubicCase(-18, 24, 3, -8) #helper-fn
    testFindIntRootsOfCubicCase(1, 2, 3, 4) #helper-fn
    print('Passed.')

#################################################
# testAll and main
#################################################

def testAll():
    # comment out the tests you do not wish to run!
    myTest()
    testDistance()
    testCirclesIntersect()
    testGetKthDigit()
    testSetKthDigit()
    testFabricYards()
    testFabricExcess()
    testThreeLinesArea()
    testColorBlender()
    testFindIntRootsOfCubic()

def main():
    cs112_n22_week1_hw1_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
