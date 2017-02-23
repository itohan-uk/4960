###############################
#   ITOHAN UKPONMWAN (iiu2)   #
#		   ECE 4960			  #
#		     HW4			  #
###############################

from copy import deepcopy
from operator import add
import numpy as np
from scipy.io import mminfo,mmread
from collections import Counter

def retrieveElement(n,rowPtr,colInd,val):
	'''Creates Sparce Matrix from Compressed row Format'''
	k = 0
	finalMat = [[0 for x in range(n)] for y in range(n)] 
	for j in range(0,((len(rowPtr))-1)): 
		for i in range((rowPtr[j]),(rowPtr[j+1])): 
			col = colInd[k]
			finalMat[j][col] = val[k]
			k = k + 1

	#for z in finalMat:
	#	print z
	
	return finalMat		


def rowPermute(mat, vec, i, j):
	'''Switch row[i] and row[j] for matrix mat and vector vec'''
	
	newMat = deepcopy(mat)
	newVec = deepcopy(vec)
	newMat[i] = mat[j]
	newMat[j] = mat[i]
	newVec[i] = vec[j]
	newVec[j] = vec[i]

	#for x in newMat:
	#	print x

	#print("\n\n")	
	#for y in newVec:
	#	print y	

	return [newMat,newVec]	




def rowScale(mat, vec, i, j, a):
	'''Add a*row[i] to row[j] for matrix A and vector x'''
	a = np.float64(a)
	newMat = deepcopy(mat)
	newVec = deepcopy(vec)

	matMult = [k*a for k in newMat[i]]
	newMat[j] = map(add, newMat[j], matMult)

	vecMult = (newVec[i]) * a
	newVec[j] = newVec[j] + vecMult

	for x in newMat:
		print x
	print("\n\n")

	for y in newVec:
		print y	


def productAx(mat,vec):
	'''Returns product of mat*vec = b'''
	mat = np.array(mat)
	vec = np.array(vec)
	b = mat.dot(vec)
	
	for k in b:
		print k



def rowPermuteCom(val,rowPtr,colInd,i,j):
	rowI = {}
	rowj = {}
	newVal = deepcopy(val)
	newrowPtr = deepcopy(rowPtr)
	newColIdx = deepcopy(colInd)

	for idx in range(rowPtr[i],rowPtr[i+1]):
		value = val[idx]
		rowI[value] = colInd[idx]

	for idx2 in range(rowPtr[j],rowPtr[j+1]):
		jvalue = val[idx2]
		rowj[jvalue] = colInd[idx2]

	

	numRowI = rowPtr[i+1] - rowPtr[i] #no of elements in rowI 
	numRowJ = rowPtr[j+1] - rowPtr[j] #no of elements in rowJ


	newrowPtr[i + 1] = rowPtr[i] + numRowJ


	
	for ptrVal in range((i + 1), ((len(rowPtr))-1)):
		diff = rowPtr[ptrVal + 1] - rowPtr[ptrVal]
		newrowPtr[ptrVal + 1] = newrowPtr[ptrVal] + diff
		if ptrVal == j:
			newrowPtr[ptrVal + 1] = newrowPtr[ptrVal] + numRowI


	numBeforeI = rowPtr[i] - rowPtr[i-1]
	numBeforeJ = rowPtr[j] - rowPtr[j-1]
	for k in range(len(rowj)):
		newVal[numBeforeI] = rowj.keys()[k]
		newColIdx[numBeforeI] = rowj.values()[k]
		numBeforeI = numBeforeI + 1
	

	rowBeforeJ = rowPtr[j] - rowPtr[i + 1]
	idxBegin = (rowPtr[i + 1])
	for x in range(rowBeforeJ):
		newVal[numBeforeI] = val[idxBegin]
		newColIdx[numBeforeI] = colInd[idxBegin]
		numBeforeI = numBeforeI + 1
		idxBegin = idxBegin + 1



	for y in range(len(rowI)):
		newVal[numBeforeI] = rowI.keys()[y]
		newColIdx[numBeforeI] = rowI.values()[y]
		numBeforeI = numBeforeI + 1


	#print newVal
	#print newrowPtr
	#print newColIdx

	return [newVal,newrowPtr,newColIdx]

#def rowScale(mat, vec, i, j, a):
	'''Add a*row[i] to row[j] for matrix A and vector x'''
#	a = np.float64(a)

def rowScaleCom(compMat,i,j,a):
	'''CompMat is list of 3 lists containing val,
	rowPtr and colInd respectively in a row compressed storage
	'''
	val = compMat[0]
	rowPtr = compMat[1]
	colInd = compMat[2]
	a = np.float64(a)
	rowIlist = []
	colIlist = []
	numRowI = rowPtr[i+1] -rowPtr[i]
	rowIdx = rowPtr[i]
	for ele in range(numRowI):
		rowIlist.append(val[rowIdx])
		colIlist.append(colInd[rowIdx])
		rowIdx = rowIdx + 1

	#add the 0s to rowIlist and their indexes
	for	i in range((len(rowPtr) - 1)):
		if i not in colIlist:
			colIlist.insert(i,i)
			rowIlist.insert(i,0)
			
	print rowIlist	
	print colIlist





def tester(fullMat, sparseMat):
	'''fullMat Contains a list of lists, each list
	   represents a row in the full matrix, sparseMat
	   contains a list of 3 lists each list representing
	   the value, rowPtr and colInd respectively in a
	   compressed row storage format'''
	fullMatList = []
	sparseMatList = sparseMat[0]
	for row in range(len(fullMat)):
		for col in range(len(fullMat[row])):
			aFull = fullMat[row][col]
			if (aFull != 0):
				fullMatList.append(aFull)

	diff = (np.array(fullMatList)) - (np.array(sparseMatList))
	squareDiff = np.square(diff)
	final = sum(squareDiff)	

	print final
	return final

			 


rowPtr = [0,3,6,9,10,12]
colInd = [0,1,4,0,1,2,1,2,4,3,0,4]
val = [1,2,3,4,5,6,7,8,9,10,11,12]
vec = [5,4,3,2,1]

B = rowPermuteCom(val,rowPtr,colInd,1,4)
mat = retrieveElement(5,rowPtr,colInd,val)
A = (rowPermute(mat,vec,1,4))[0]


#tester(A,B)
#rowScale(mat,vec,1,4,3)
compMat = [val,rowPtr,colInd]
rowScaleCom(compMat,1,4,3)