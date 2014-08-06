import math
import operator
import re

def gcd(a, b):
	r0 = a
	r1 = b
	while r1 != 0:
		q = math.floor(float(r0)/r1)
		temp = r0
		r0 = r1
		temp_r = r1
		r1 = temp - (q*r1)

	return temp_r

def multiplicative_inv(a, b):
	a0 = a
	b0 = b
	t0 = 0
	t = 1
	q = math.floor(float(a0)/b0)
	r = a0 - (q*b0)

	while r > 0:
		temp = (t0 - (q*t)) % a 
		t0 = t
		t = temp
		a0 = b0
		b0 = r
		q = math.floor(float(a0)/b0)
		r = a0 - (q*b0)

	if(b0 != 1):
		return -9999
	else:
		return t
		
pattern = re.compile(r"\s+")
f = open("caffine.txt", "r")

ciphertext = ""

for line in f:
	ciphertext += line

ciphertext = re.sub(pattern, "", ciphertext)
print "\nCiphertext:\n%s" % ciphertext

mappings = {}

for c in ciphertext:
	c = c.upper()
	mappings[c] = mappings.get(c, "-")

c11 = raw_input("\nEnter the first character to replace: ")
c12 = raw_input("Enter the first new character: ")
c21 = raw_input("Enter the second character to replace: ")
c22 = raw_input("Enter the second new character: ")

c11 = c11.upper()
c12 = c12.upper()
c21 = c21.upper()
c22 = c22.upper()

alpha = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J", 10:"K", 11:"L", 12:"M", 13:"N", 14:"O", 15:"P", 16:"Q", 17:"R", 18:"S", 19:"T", 20:"U", 21:"V", 22:"W", 23:"X", 24:"Y", 25:"Z"}

numerical = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9, "K":10, "L":11, "M":12, "N":13, "O":14, "P":15, "Q":16, "R":17, "S":18, "T":19, "U":20, "V":21, "W":22, "X":23, "Y":24, "Z":25} 

replace0 = numerical[c11]
new0 = numerical[c12]
replace1 = numerical[c21]
new1 = numerical[c22]

print "\nCalculations:"

if new0 > new1:
	sub0 = new0 - new1
	sub1 = (replace0 - replace1) % 26
	print "Calculating %da = %d mod 26" % (sub0, sub1)
else:
	sub0 = new1 - new0
	print "%d(%s) - %d(%s)" % (replace1, c21, replace0, c11)
	sub1 = (replace1 - replace0) % 26
	print "Calculating %da = %d mod 26" % (sub0, sub1)


sub0_inv = multiplicative_inv(26, sub0)

if sub0_inv != -9999:
	a = (sub1*sub0_inv) % 26

	print "Multiply both sides by the multiplicative inverse"
	print "We now have: a = %d mod 26" % a
	print "a is %d in Z_26" % a

	if gcd(26, a) == 1:
		print "We find that gcd(26, %d) = 1, so this is a valid cipher" % a

		#back substitute to find b
		b = (replace0 - (new0*a)) % 26
		print "Solving for b we have b = %d mod 26" % b
		print "b is %d in Z_26" % b

		#the key
		print "So K=(a,b)=(%d,%d)" % (a, b)

		#determine the decryption function	
		a_inv = multiplicative_inv(26, a)

		#if the inverse exists
		if a_inv != -9999:
			a_inv = a_inv % 26
			print "So decryption function is:"
			print "d(y) = %d (y-%d) mod 26" % (a_inv, b)
			b = -1*b
			b = (a_inv*b) % 26
			print "d(y) = (%dy + %d) mod 26" % (a_inv, b)

			for item in mappings:
				c = ((a_inv*numerical[item[0]]) + b) % 26
				mappings[item[0]] = alpha[c] 	

			print "\nMappings from ciphertext to plaintext elements:"
			for key, value in mappings.iteritems():
				print "%s -> %s" % (key, value.lower())
		else:
			print "%d (mod 26) has no multiplicative inverse" % a

	else:
		print "gcd(26 %d) != 1 so this is not a valid cipher" % a
else:
	print "%d (mod 26) has no multiplicative inverse" % sub0
