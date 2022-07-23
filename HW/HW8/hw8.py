#################################################
# hw8.py
#
# Your name: Zack
# Your andrew id: ysima
#################################################

import cs112_n22_week4_linter

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
# # hw8-standard classes for you to write
#################################################

#person class
class Person(object):
    #constructor
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.friends = []

    #get methods
    def getName(self):
        return self.name
    def getAge(self):
        return self.age
    def getFriends(self):
        if self.friends == []:
            return None
        return self.friends

    #add methods
    def addFriend(self, friend):
        if friend not in self.friends and friend != self:
            self.friends.append(friend)

#tester for debug
def test():
    fred = Person('fred', 32)
    wilma = Person('wilma', 35)
    barney = Person('barney', 28)
    wilma.addFriend(fred)
    fred.addFriend(wilma)
    fred.addFriend(barney)


#################################################
# Bonus/Optional classes
#################################################

class Bird(object):
    pass

class Penguin(Bird):
    pass

class MessengerBird(Bird):
    pass

#################################################
# Test Functions
#################################################

def testPersonClass():
    print('Testing Person Class...', end='')
    fred = Person('fred', 32)
    assert(isinstance(fred, Person))
    assert(fred.getName() == 'fred')
    assert(fred.getAge() == 32)
    assert(fred.getFriends() == None)

    wilma = Person('wilma', 35)
    assert(wilma.getName() == 'wilma')
    assert(wilma.getAge() == 35)
    assert(wilma.getFriends() == None)

    wilma.addFriend(fred)
    assert(wilma.getFriends() == [fred]) # fred is a variable name, not a string
    assert(fred.getFriends() == None) # friends are not necessarily reciprocal!
    wilma.addFriend(fred)
    assert(wilma.getFriends() == [fred]) # don't add twice!

    barney = Person('barney', 28)
    fred.addFriend(wilma)
    fred.addFriend(barney)
    assert(fred.getFriends() == [wilma, barney])
 
    fred.addFriend(barney)  # don't add twice
    fred.addFriend(fred)    # ignore self as a friend
    assert(fred.getFriends() == [wilma, barney])
    print('Passed!')

def getLocalMethods(clss):
    import types
    # This is a helper function for the test function below.
    # It returns a sorted list of the names of the methods
    # defined in a class. It's okay if you don't fully understand it!
    result = [ ]
    for var in clss.__dict__:
        val = clss.__dict__[var]
        if (isinstance(val, types.FunctionType)):
            result.append(var)
    return sorted(result)

def testBirdClasses():
    print("Testing Bird classes...", end="")
    # A basic Bird has a species name, can fly, and can lay eggs
    bird1 = Bird("Parrot")
    assert(type(bird1) == Bird)
    assert(isinstance(bird1, Bird))
    assert(bird1.fly() == "I can fly!")
    assert(bird1.countEggs() == 0)
    assert(str(bird1) == "Parrot has 0 eggs")
    bird1.layEgg()
    assert(bird1.countEggs() == 1)
    assert(str(bird1) == "Parrot has 1 egg")
    bird1.layEgg()
    assert(bird1.countEggs() == 2)
    assert(str(bird1) == "Parrot has 2 eggs")
    tempBird = Bird("Parrot")
    assert(bird1 == tempBird)
    tempBird = Bird("Wren")
    assert(bird1 != tempBird)
    assert(getLocalMethods(Bird) == ['__eq__','__init__', 
                                 '__repr__', 'countEggs', 
                                 'fly', 'layEgg'])
    
    # A Penguin is a Bird that cannot fly, but can swim
    bird2 = Penguin("Emperor Penguin")
    assert(type(bird2) == Penguin)
    assert(isinstance(bird2, Penguin))
    assert(isinstance(bird2, Bird))
    assert(not isinstance(bird1, Penguin))
    assert(bird2.fly() == "No flying for me.")
    assert(bird2.swim() == "I can swim!")
    bird2.layEgg()
    assert(bird2.countEggs() == 1)
    assert(str(bird2) == "Emperor Penguin has 1 egg")
    assert(getLocalMethods(Penguin) == ['fly', 'swim'])
    
    # A MessengerBird is a Bird that carries a message
    bird3 = MessengerBird("War Pigeon", "Top-Secret Message!")
    assert(type(bird3) == MessengerBird)
    assert(isinstance(bird3, MessengerBird))
    assert(isinstance(bird3, Bird))
    assert(not isinstance(bird3, Penguin))
    assert(not isinstance(bird2, MessengerBird))
    assert(not isinstance(bird1, MessengerBird))
    assert(bird3.deliverMessage() == "Top-Secret Message!")
    assert(str(bird3) == "War Pigeon has 0 eggs")
    assert(bird3.fly() == "I can fly!")

    bird4 = MessengerBird("Homing Pigeon", "")
    assert(bird4.deliverMessage() == "")
    bird4.layEgg()
    assert(bird4.countEggs() == 1)
    assert(getLocalMethods(MessengerBird) == ['__init__', 'deliverMessage'])

    # Note: all birds are migrating or not (together, as one)
    assert(bird1.isMigrating == bird2.isMigrating == bird3.isMigrating == False)
    assert(Bird.isMigrating == False)

    bird1.startMigrating()
    assert(bird1.isMigrating == bird2.isMigrating == bird3.isMigrating == True)
    assert(Bird.isMigrating == True)

    Bird.stopMigrating()
    assert(bird1.isMigrating == bird2.isMigrating == bird3.isMigrating == False)
    assert(Bird.isMigrating == False)
    print("Passed!")

#################################################
# testAll and main
#################################################

def testAll():
    test()
    testPersonClass()
    #testBirdClasses()

def main():
    cs112_n22_week4_linter.lint()
    testAll()

if (__name__ == '__main__'):
    main()
