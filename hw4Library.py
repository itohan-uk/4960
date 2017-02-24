###############################
#   ITOHAN UKPONMWAN (iiu2)   #
#		   ECE 4960			  #
#		 HW4	LIBRARY		  #
###############################

from copy import deepcopy
from operator import add
import numpy as np
from scipy.io import mminfo,mmread
import json

def retrieveElement(n,rowPtr,colInd,val):
	'''Creates Sparce Matrix from Compressed row Format'''
	k = 0
	finalMat = [[0 for x in range(n)] for y in range(n)] 
	for j in range(0,((len(rowPtr))-1)): 
		for i in range((rowPtr[j]),(rowPtr[j+1])): 
			col = colInd[k]
			finalMat[j][col] = val[k]
			k = k + 1	
	return finalMat		


def rowPermute(mat, vec, i, j):
	'''Switch row[i] and row[j] for full matrix mat and vector vec'''
	
	newMat = deepcopy(mat)
	newVec = deepcopy(vec)
	newMat[i] = mat[j]
	newMat[j] = mat[i]
	newVec[i] = vec[j]
	newVec[j] = vec[i]


	return [newMat,newVec]	




def rowScale(mat, vec, i, j, a):
	'''Add a*row[i] to row[j] for full matrix mat and vector vec'''
	a = np.float64(a)
	newMat = deepcopy(mat)
	newVec = deepcopy(vec)

	matMult = [k*a for k in newMat[i]]
	newMat[j] = map(add, newMat[j], matMult)

	vecMult = (newVec[i]) * a
	newVec[j] = newVec[j] + vecMult

	return [newMat,newVec]	


def productAx(mat,vec):
	'''Returns product of full Matrix mat*vec = b'''
	mat = np.array(mat)
	vec = np.array(vec)
	b = mat.dot(vec)
	
	return b



def rowPermuteCom(compMat,vec,i,j):	
	'''Switch row[i] and row[j] for compressed row matrix compMat and vector vec'''
	rowI = {}
	rowj = {}
	val = compMat[0]
	rowPtr = compMat[1]
	colInd = compMat[2]
	newVec = deepcopy(vec)
	newVal = deepcopy(val)
	newrowPtr = deepcopy(rowPtr)
	newColIdx = deepcopy(colInd)

	for idx in range((int(rowPtr[i])),(int(rowPtr[i+1]))):
		value = val[idx]
		rowI[value] = colInd[idx]

	for idx2 in range((int(rowPtr[j])),(int(rowPtr[j+1]))):
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
	for x in range(int(rowBeforeJ)):
		newVal[numBeforeI] = val[idxBegin]
		newColIdx[numBeforeI] = colInd[idxBegin]
		numBeforeI = numBeforeI + 1
		idxBegin = idxBegin + 1



	for y in range(len(rowI)):
		newVal[numBeforeI] = rowI.keys()[y]
		newColIdx[numBeforeI] = rowI.values()[y]
		numBeforeI = numBeforeI + 1


	
	#Permute Vector Elements
	newVec[i] = vec[j]
	newVec[j] = vec[i]
	newCompMat = [newVal,newrowPtr,newColIdx]
	
	#Return Statement
	return [newCompMat,newVec]



def rowScaleCom(compMat,vec,i,j,a):
	'''CompMat is a list of 3 lists containing val,
	rowPtr and colInd respectively in a row compressed storage
	'''
	val = compMat[0]
	newVal = deepcopy(val)
	newVec = deepcopy(vec)
	rowPtr = compMat[1]
	newrowPtr = deepcopy(rowPtr)
	colInd = compMat[2]
	newColInd = deepcopy(colInd)
	newRowJvals = []
	a = np.float64(a)
	rowIlist = []
	rowJlist = []
	colIlist = []
	colJlist = []
	numRowI = rowPtr[i+1] -rowPtr[i]
	numRowJ = rowPtr[j+1] -rowPtr[j]
	rowIdx = rowPtr[i]
	rowJdx = rowPtr[j]
	for ele in range(int(numRowI)):
		rowIlist.append(val[rowIdx])
		colIlist.append(colInd[rowIdx])
		rowIdx = rowIdx + 1

	#add the 0s to rowIlist and their indexes
	for	i in range((len(rowPtr) - 1)):
		if i not in colIlist:
			colIlist.insert(i,i)
			rowIlist.insert(i,0)
	


	#GetrowJ elements and their indexes
	for elj in range(int(numRowJ)):
		rowJlist.append(val[rowJdx])
		colJlist.append(colInd[rowJdx])
		rowJdx = rowJdx + 1

	#add 0s to rowJlist and their indexes
	for	idx in range((len(rowPtr) - 1)):
		if idx not in colJlist:
			colJlist.insert(idx,idx)
			rowJlist.insert(idx,0)	

	addToJ = a*(np.array(rowIlist))
	newRowJ = addToJ + (np.array(rowJlist))
	
	#make a list of non zero elements in rowJ
	for value in newRowJ:
		if value != 0:
			newRowJvals.append(value)

	#Edit new RowPtr to make for change in no of elements
	for x in range(1,((len(rowPtr)) - j)):
		newrowPtr[j+1] = newrowPtr[j] + len(newRowJvals)


	#Edit row ptr vals after j
	for rowPtrVal in range((j+2), (len(rowPtr))):
		newrowPtr[rowPtrVal] = newrowPtr[rowPtrVal -1]	+ (rowPtr[rowPtrVal] -rowPtr[rowPtrVal-1])
		

	#index that val starts changing
	valchangeIdx = rowPtr[j]

	#Elements increased by
	numNew = (newrowPtr[(len(newrowPtr)) -1]) - (rowPtr[(len(rowPtr)) -1]) 
	if numNew <= 0:
		numNew = 0

		
	for newV in range((len(newRowJvals)) - numNew):
		newVal[valchangeIdx] = newRowJvals[newV]
		newColInd[valchangeIdx] = colJlist[(list(newRowJ)).index(newRowJvals[newV])]
		valchangeIdx = valchangeIdx + 1
	
	if numNew > 0:
		for v in range(numNew):
			newVal.insert(valchangeIdx,newRowJvals[newV + v + 1])
			newColInd.insert(valchangeIdx, (colJlist[(list(newRowJ)).index(newRowJvals[newV + v + 1])]))
			valchangeIdx = valchangeIdx + 1
	

	vecMult = (newVec[i]) * a
	newVec[j] = newVec[j] + vecMult



	newCompMat = [newVal,newrowPtr,newColInd]
	return [newCompMat,newVec]



def productAxComp(compMat,vec):
	'''Returns the product of a compressed row Matrix
	compMat and a vector vec'''
	
	
	val = compMat[0]
	rowPtr = compMat[1]
	colInd = compMat[2]
	b = [] #b is a vector containing compMat*Vec

	value = 0 #used to index val
	for num in range((len(rowPtr)) -1):
		rowSum = 0
		for k in range((rowPtr[num +1]) - (rowPtr[num])):
			rowSum = rowSum + (val[value] * vec[int(colInd[value])])
			value = value + 1
			
		b.append(rowSum)
	
	
	return np.array(b)

def coordTOrow(cordMat):
	'''Converts a matrix cordMat from Co-ordinate Storage Format to Row Compressed
	 Co-ordinate storage format is in the form of col,row,value'''
	colInd = cordMat[0]
	vals = cordMat[2]
	rowPtr = [0]

	count = 1
	for rowVal in  range(1,((len(cordMat[1])))):
		if((cordMat[1][rowVal]) == (cordMat[1][rowVal -1])):
			count = count + 1
		else:
			rowPtr.append(count)
			count = count + 1
	rowPtr.append(len(cordMat[0]))
	#print([vals, rowPtr, colInd])			

	return [vals, rowPtr, colInd]			









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

	
	return final

			 

with open('memplus.mtx') as largeMtx:
	horizontal = [line.split() for line in largeMtx]

horizontal.pop(0)
horizontal.pop(0)
vertical = zip(*horizontal)
bigMat = [map(float, vline) for vline in vertical[0:]]


for no in range(len(bigMat[0])):
	bigMat[0][no] = (bigMat[0][no]) - 1
	bigMat[1][no] = (bigMat[1][no]) - 1



