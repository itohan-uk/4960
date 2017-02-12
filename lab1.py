import numpy as np
from decimal import Decimal, getcontext
import logging
import warnings
from math import factorial

getcontext().prec = 40

#warnings.simplefilter("error", RuntimeWarning)
	
def integerOverflow():
	intFactorial = np.uint32(1)
	for i in range(1,30):
		try:
			intFactorial = intFactorial * i
			print(i, intFactorial)
		except RuntimeWarning, e:
			file = open('EngineerReport.txt','w')
			file.write("############################\n# INTEGER OVERFLOW TESTING #\n############################\n")
			file.write("Runtime Warning Error below occured at iteration %d\n##%s##\n\n"%(i,e))
			file.close()
			print(i, intFactorial)	
	print ("\n")
	

def integerDivideZero():
	num1 = 5
	zero = 0
	try:
		val = num1/zero
	except ZeroDivisionError, e:
		file = open('EngineerReport.txt','a')
		file.write("####################################\n# INTEGER DIVISION BY ZERO TESTING #\n####################################\n")
		file.write("The ZeroDivisionError below occured \n##%s##\n\n"%e)
		file.close()
	print ("\n")
	

def floatOverflow():
	float1 = np.float64(1.02)

	for i in range(1,200):
		try:
			float1 = float1 * i
			print "%d, %.30f" %(i, float1)
		except RuntimeWarning, e:
			file = open('EngineerReport.txt','a')
			file.write("###########################\n# FLOAT OVERFLOW TESTING #\n###########################\n")
			file.write("Runtime Warning Error below occured at iteration %d\n##%s##\n\n"%(i,e))
			file.close()
			print "%d, %.30f" %(i, float1)
			break
	print ("\n")
	

def floatOpINF():
	val1 = np.inf
	val2 = -np.inf
	
	try:
		test1 = np.sin(val1)
	except RuntimeWarning, e:
		file = open('EngineerReport.txt','a')
		file.write("###############################\n# FLOAT INF AND NINF TESTING #\n###############################\n")
		file.write("Runtime Warning Error below occured \n##%s##\n\n"%(e))
		
	test2 = 1/ val1
	test3 = np.exp(val1)

	try:
		test4 = np.sin(val2)

	except RuntimeWarning, e:
		file.write("Runtime Warning Error below occured \n##%s##\n\n"%(e))
		file.close()	
	
	test5 = 1/val2
	test6 = np.exp(val2)
	
	print test1
	print test2
	print test3
	print test4
	print test5
	print test6
	print ("\n")


def floatOpNAN():
	#nan1 = np.nan
	#nan1 = np.float64(np.sqrt(-1.0))
	nan1 = (np.inf/np.inf)
	print nan1
	print np.isnan(nan1)
	print ("\n")



def signedZero():
	pZero = 1.0/(np.inf)
	nZero = 1.0/(-np.inf)
	file = open('EngineerReport.txt','a')
	file.write("###############################\n# SIGNED ZERO TESTING #\n###############################\n")
	try:
		plog = np.log(pZero)
	except RuntimeWarning, e:
		file.write("Runtime Warning Error below occured \n##%s##\n\n"%(e))

	try:
		nlog = np.log(nZero)
	except RuntimeWarning, e:
		file.write("Runtime Warning Error below occured \n##%s##\n\n"%(e))	
	
	pSin = (np.sin(pZero))/pZero
	nSin = (np.sin(nZero))/nZero

	aSin = (np.sin(nZero))/abs(nZero)

	print plog
	print nlog
	print pSin
	print nSin
	print aSin
	print ("\n")


#def floatSoftLand():
'''
def factorial(n):
	if (n == 0) or (n==1):
		fact = 1
	else:
		fact = n * factorial(n -1)
	return fact	'''


def piCalculator():
	prec = 25
	a = Decimal(0) 
	
	for k in range(prec):
		b = ((-1)**k)*(factorial(6*k)) * (13591409 +(545140134*k))
		c = (factorial(3*k))*((factorial(k))**3)
		d = 640320 **((3*k) + Decimal(1.5))
		a = Decimal(a) +((Decimal(b))/(Decimal((Decimal(c))*(Decimal(d)))))
	final = Decimal(12) * Decimal(a)	
	pi = Decimal(1)/Decimal(final)

	return pi


'''def calculatePi():
	a = np.power(5280,3)
	b = np.power(Decimal(236674) + (((30303 * (np.sqrt(61))))),3)
	c = 744
	d = np.sqrt(427)
	pi = (np.log((a*b) + c))/d
	return pi


print ("%.30f" %calculatePi())'''

#integerOverflow()
#integerDivideZero()
#floatOverflow()
#floatOpINF()
#floatOpNAN()
#signedZero()
#print factorial(5)
print piCalculator()