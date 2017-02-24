###############################
#   ITOHAN UKPONMWAN (iiu2)   #
#		   ECE 4960			  #
#		 HW4	PART1		  #
###############################





import hw4Library as hp
import numpy as np




#Test Values
aFull = [[1,2,0,0,3],[4,5,6,0,0],[0,7,8,0,9],[0,0,0,10,0],[11,0,0,0,12]]
aSparse = [[1,2,3,4,5,6,7,8,9,10,11,12],[0,3,6,9,10,12],[0,1,4,0,1,2,1,2,4,3,0,4]]
xVector = [5,4,3,2,1]


#Part 1 Test1
#Permutation of (1,3)
print ("Permutation of row(1,3) Using Full Matrix and Sparse Matrix Format")
i,j = 1,3
aFullp13 = (hp.rowPermute(aFull,xVector,i,j))[0]
aSparsep13 = (hp.rowPermuteCom(aSparse,xVector,i,j))[0]
print("Results of Differrence Test:")
print hp.tester(aFullp13,aSparsep13)

print("________________________________________________________________________________")

#Permutation of (1,4) after (1,3)
print("Permutation of row(1,4) from Results of Permutation of row(1,3) Using Full Matrix and Sparse Matrix Format")
i,j = 1,4
aFullp14 = (hp.rowPermute(aFullp13,xVector,i,j))[0]
aSparsep14 = (hp.rowPermuteCom(aSparsep13,xVector,i,j))[0]
print("Results of Differrence Test:")
print hp.tester(aFullp14,aSparsep14)
print("________________________________________________________________________________")

#Part 1 Test 2
#Case 1
print("Testing 3*row[1] + row[4] Using Full Matrix and Sparse Matrix Format")
a = 3
i,j = 1,4

aFullS14  = (hp.rowScale(aFull,xVector,i,j,a))[0]
aSparseS14 = (hp.rowScaleCom(aSparse,xVector,i,j,a))[0]
print("Results of Differrence Test:")
print hp.tester(aFullS14,aSparseS14)
print("________________________________________________________________________________")

#Case 2
print("Testing -4.4*row[5] + row[2] with Results from 3*row[1] + row[4] Using Full Matrix and Sparse Matrix Format")
a = -4.4
i,j = 4,2
aFullS42  = (hp.rowScale(aFullS14,xVector,i,j,a))[0]
aSparseS42 = (hp.rowScaleCom(aSparseS14,xVector,i,j,a))[0]
print("Results of Differrence Test:")
print hp.tester(aFullS42,aSparseS42)
print("________________________________________________________________________________")



#Test 3
print("Testing Ax=b Using Full Matrix and Sparse Matrix Format")
aFullProd = hp.productAx(aFull, xVector)
aSparseProd = hp.productAxComp(aSparse,xVector)
print("Results of Differrence Test:")
print((np.array(aFullProd)) -(aSparseProd))


















