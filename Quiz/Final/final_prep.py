def isPrime(n):
	if n == 2:
		return True
	if n < 2:
		return False
	for i in range(2, n):
		if n % i == 0:
			return False
	return True

def isEmirpNumber(n):
	if int(str(n)[::-1]) != n and isPrime(n) and isPrime(int(str(n)[::-1])):
		return True
	return False

def nthEmirpNumber(n):
	num = 1
	while n >= 0:
		if isEmirpNumber(num):
			if n == 0:
				return num
			n -= 1
		num += 1

class Waterbottle:
	def __init__(self, color, material):
		self.color = color
		self.material = material
		self.clout = -1
	def dent(self):
		self.clout -= 1
	def paint(self, color):
		if self.color == color:
			return "Cannot paint bottle the same color"
		else:
			self.color = color
	def __eq__(self, other):
		return self.color == other.color and self.material == other.material
class Hydroflask(Waterbottle):
	def __init__(self, color, size):
		super().__init__(color, "metal")
		self.size = size
		self.clout = size
	def dent(self):
		self.size -= 1
		self.clout = self.size
	def paint(self, color):
		if super().paint(color) == None:
			self.dent()
	def eq(self, other):
		if not isinstance(other, Hydroflask):
			return False

		return self.color == other.color

def testWaterbottleAndHydroflaskClasses():
	print('Testing Waterbottle and Hydroflask classes...', end = '')
	plasticBottle = Waterbottle("blue", "plastic")
	assert((plasticBottle.color == "blue") and (plasticBottle.material == "plastic"))
	#all regular waterbottles have negative -1 clout :(
	assert(plasticBottle.clout == -1)
	metalBottle = Waterbottle("green", "metal")
	assert((metalBottle.color == "green") and (metalBottle.material == "metal") and (metalBottle.clout == -1))
	for i in range(3):
		plasticBottle.dent()
	#denting your waterbottle reduces clout
	assert(plasticBottle.clout == -4)
	assert(metalBottle.paint("green") == "Cannot paint bottle the same color")
	metalBottle.paint("blue")
	assert(metalBottle.color == "blue")
	#two bottles are the same if their color and material is the same
	assert(plasticBottle != metalBottle)
	coolerHydro = Hydroflask("purple", 24)
	assert(isinstance(coolerHydro, Waterbottle))
	assert((coolerHydro.color == "purple") and (coolerHydro.size == 24))
	#all hydros are metal and have clout equal to their size
	assert((coolerHydro.material == "metal") and (coolerHydro.clout == 24))
	coolerHydro.dent()
	assert(coolerHydro.clout == 23)
	coolerHydro.paint("green")
	#painting your hydro reduces your clout too!
	assert((coolerHydro.clout == 22) and (coolerHydro.color == "green"))
	sameHydro = Hydroflask("green", 36)
	#two hydros are equal if they have the same color
	assert(sameHydro == coolerHydro)
	#a hydro is never equal to a regular waterbottle
	assert(sameHydro != metalBottle)
	print('Passed!')


def testNthEmirpNumber():
	# 11 is not an emirp number because it’s the same forwards as backwards
	print('Testing nthEmirpNumber...', end = '')
	assert(nthEmirpNumber(0) == 13)
	assert(nthEmirpNumber(1) == 17)
	assert(nthEmirpNumber(2) == 31)
	assert(nthEmirpNumber(3) == 37)
	assert(nthEmirpNumber(4) == 71)
	assert(nthEmirpNumber(5) == 73)
	assert(nthEmirpNumber(6) == 79)
	assert(nthEmirpNumber(7) == 97)
	assert(nthEmirpNumber(8) == 107)
	assert(nthEmirpNumber(9) == 113)
	assert(nthEmirpNumber(100) == 3067)
	print('Passed!')

def only112(L):
	if L == []:
		return []
	if "112" in str(L[0]) and isinstance(L[0], int):
		return [L[0]] + only112(L[1:])
	else:
		return only112(L[1:])

def testOnly112():
	print('Testing only112...', end = '')
	L = [42, 112, 591, 15112, 79, 15213, 112]
	assert(only112(L) == [112, 15112, 112])
	L = [150, 96, 122, 112121212]
	assert(only112(L) == [112121212])
	L = [213, 224, 911, '112']
	assert(only112(L) == [])
	L = ['croaking', 'in', 'pizza romano', 'at', 112, 'AM']
	assert(only112(L) == [112])
	print('Passed!')

testOnly112()