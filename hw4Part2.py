###############################
#   ITOHAN UKPONMWAN (iiu2)   #
#		   ECE 4960			  #
#		 HW4	PART2	      #
###############################





import hw4Library as hp
import numpy as np
import time
from guppy import hpy


start = time.clock()
mem = hpy()

print("###MEMORY USAGE AT THE BEGINNNG OF THE SCRIPT###")
print mem.heap()
print("\n\n")
#PART 2
#Get mtx File and put in desired format
with open('memplus.mtx') as largeMtx:
	horizontal = [line.split() for line in largeMtx]

horizontal.pop(0)
horizontal.pop(0)
vertical = zip(*horizontal)
bigMat = [map(float, vline) for vline in vertical[0:]]

for no in range(len(bigMat[0])):
	bigMat[0][no] = (bigMat[0][no]) - 1
	bigMat[1][no] = (bigMat[1][no]) - 1

#Convert bigMat to row Compressed Format
newbigMat = hp.coordTOrow(bigMat)
bigVec = [1] * (len(newbigMat[0]))

'''#permutation Tests
#print("Permutation of row(1,3) of mtx Matrix")
result1 = (hp.rowPermuteCom(newbigMat,bigVec,1,3))[0]
#print result1


#Permutation of row(1,5) of mtx Matrix from results of permutation of (1,3)
#print("Permutation of row(1,5) of mtx Matrix from results of permutation of (1,3)")
result2 = (hp.rowPermuteCom(result1,bigVec,1,5))[0]

#Permutation of row(10,3000) of mtx Matrix from results of permutation of (1,5)
#print("Permutation of row(10,3000) of mtx Matrix from results of permutation of (1,5)")
result3 = (hp.rowPermuteCom(result2,bigVec,10,3000))[0]

#Permutation of row(5000,10000) of mtx Matrix from results of permutation of (10,3000)
#print("Permutation of row(5000,10000) of mtx Matrix from results of permutation of (10,3000)")
result4 = (hp.rowPermuteCom(result3,bigVec,5000,10000))[0]

#Permutation of row(6,15000) of mtx Matrix from results of permutation of (5000,10000)
#print("Permutation of row(6,15000) of mtx Matrix from results of permutation of (5000,10000)")
result4 = (hp.rowPermuteCom(result3,bigVec,6,15000))[0]'''


#Tests 2
#Row Scaling Tests
#Test 2.1
#3.0*row[2] + row[4]

#scale1 = (hp.rowScaleCom(newbigMat,bigVec,2,4,3))[0]

#Test 2.1.1
#permute(2,5) of scale1 result
#scale2 = (hp.rowPermuteCom(scale1,bigVec,2,5))[0]

#Test 2.1.2
#-3.0*row[5] + row[4] using scale2
#scale3 = (hp.rowScaleCom(scale2,bigVec,5,4,-3))[0]


#Test 3
#Ax = b
scale4 = hp.productAxComp(newbigMat,bigVec)


#Test 4
print("Performing Difference Test between A and Ax = b")
sumA = sum(newbigMat[0])
sumB = sum(scale4)

diffTest = abs(sumA - sumB)
print("Result:")
print diffTest

elapsedTime = (time.clock() - start)
print("\n\n")
print("Elapsed Time: %f Seconds" %elapsedTime)
print("\n\n")


#print usedMemory
print("###MEMORY USAGE AT THE END OF THE SCRIPT###")
print mem.heap()