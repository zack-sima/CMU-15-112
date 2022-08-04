#################################################
# hw12.py
#
# Your name:
# Your andrew id:
#################################################

import cs112_n22_hw12_linter
import math, copy

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

def evalPrefixNotation(L):
    return helperEvalPrefixNotation(L, 0)[0]

def helperEvalPrefixNotation(L, index):
    if isinstance(L[index], int):
        #if integer, return said integer and next index
        return L[index], index + 1

    #symbols
    first, nextIndex = helperEvalPrefixNotation(L, index + 1)
    second, finalIndex = helperEvalPrefixNotation(L, nextIndex)

    if L[index] == "+":
        return first + second, finalIndex
    elif L[index] == "-":
        return first - second, finalIndex
    elif L[index] == "*":
        return first * second, finalIndex
    else:
        raise Exception("Unknown operator: " + L[index])

def myTest():
    myTour = knightsTour(5, 5)
    if myTour != None:
        for i in myTour:
            print(i)
    else:
        print("None")
    #print(evalPrefixNotation(["+", "*", 1, 2, "*", 2, 3]))

def findLegalMoves(grid, row, col):
    #knight pattern
    moves = [
    (row - 1, col - 2), (row - 2, col - 1),
    (row - 1, col + 2), (row - 2, col + 1),
    (row + 1, col - 2), (row + 2, col - 1),
    (row + 1, col + 2), (row + 2, col + 1)
    ]
    legalMoves = []
    for location in moves:
        if location[0] < 0 or location[0] >= len(grid) or\
        location[1] < 0 or location[1] >= len(grid[0]):
            continue

        #unoccupied
        if grid[location[0]][location[1]] == 0:
            legalMoves.append((location[0], location[1]))

    return legalMoves #empty if no moves left

def boardIsFilled(grid):
    for i in grid:
        for j in i:
            if j == 0:
                return False
    return True

def helperKnightsTour(grid, row, col, step=1):
    grid[row][col] = step

    legalMoves = findLegalMoves(grid, row, col)
    if legalMoves == []:
        if boardIsFilled(grid):
            return True
        return False #no moves
    for move in legalMoves:
        #print(("  " * (step - 1)) + str(row) + ", " + str(col))
        print(" " * step + str(row) + ", " + str(col))
        if helperKnightsTour(grid, move[0], move[1], step=step + 1):
            return True
        else:
            #backtrack
            grid[move[0]][move[1]] = 0

    return False

def createNewBoard(rows, cols):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            grid[i].append(0)
    return grid

def knightsTour(rows, cols):
    #try placing the knight at every location,
    #but we just test 0, 0 first

    for i in range(rows):
        for j in range(cols):
            grid = createNewBoard(rows, cols)
            helperKnightsTour(grid, i, j)
            if boardIsFilled(grid):
                return grid
    return None

#################################################
# Test Functions
#################################################

def testEvalPrefixNotation():
    print('Testing evalPrefixNotation()...', end='')
    assert(evalPrefixNotation([42]) == 42)          # (42)
    assert(evalPrefixNotation(['+', 3, 4]) == 7)    # (3 + 4)
    assert(evalPrefixNotation(['-', 3, 4]) == -1)   # (3 - 4)
    assert(evalPrefixNotation(['-', 4, 3]) == 1)    # (4 - 3)
    assert(evalPrefixNotation(['+', 3, '*', 4, 5]) == 23)   # (3 + (4 * 5))

    # ((2 * 3) + (4 * 5))
    assert(evalPrefixNotation(['+', '*', 2, 3, '*', 4, 5]) == 26)
    # ((2 + 3) * (4 + 5))
    assert(evalPrefixNotation(['*', '+', 2, 3, '+', 4, 5]) == 45)
    # ((2 + (3 * (8 - 7))) * ((2 * 2) + 5))
    assert(evalPrefixNotation(['*', '+', 2, '*', 3, '-', 8, 7,
                               '+', '*', 2, 2, 5]) == 45)
    
    #Make sure to raise an error for operators that are not +, -, or *
    raisedAnError = False
    try:
        evalPrefixNotation(['^', 2, 3])
    except:
        raisedAnError = True
    assert(raisedAnError == True)
    print('Passed.')


def testKnightsTour():
    print('Testing knightsTour()....', end='')
    def checkDims(rows, cols, ok=True):
        T = knightsTour(rows, cols)
        s = f'knightsTour({rows},{cols})'
        if (not ok):
            if (T is not None):
                raise Exception(f'{s} should return None')
            return True
        if (T is None):
            raise Exception(f'{s} must return a {rows}x{cols}' +
                             ' 2d list (not None)')
        if ((rows != len(T)) or (cols != (len(T[0])))):
            raise Exception(f'{s} must return a {rows}x{cols} 2d list')
        d = dict()
        for r in range(rows):
            for c in range(cols):
                d[ T[r][c] ] = (r,c)
        if (sorted(d.keys()) != list(range(1, rows*cols+1))):
            raise Exception(f'{s} should contain numbers' +
                             ' from 1 to {rows*cols}')
        prevRow, prevCol = d[1]
        for step in range(2, rows*cols+1):
            row,col = d[step]
            distance = abs(prevRow - row) + abs(prevCol - col)
            if (distance != 3):
                raise Exception(f'{s}: from {step-1} to {step}' +
                                 ' is not a legal move')
            prevRow, prevCol = row,col
        return True
    assert(checkDims(4, 3))
    assert(checkDims(4, 4, ok=False))
    assert(checkDims(4, 5))
    assert(checkDims(3, 4))
    assert(checkDims(3, 6, ok=False))
    assert(checkDims(3, 7))
    assert(checkDims(5, 5))
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    myTest()
    #testEvalPrefixNotation()
    #testKnightsTour()
def main():
    cs112_n22_hw12_linter.lint()
    testAll()

if (__name__ == '__main__'):
    main()
