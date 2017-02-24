###############################
#   ITOHAN UKPONMWAN (iiu2)   #
#		   ECE 4960			  #
#		     HW4			  #
###############################

from copy import deepcopy
from operator import add
import numpy as np
from scipy.io import mminfo,mmread


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
	'''Switch row[i] and row[j] for full matrix mat and vector vec'''
	
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
	'''Add a*row[i] to row[j] for full matrix mat and vector vec'''
	a = np.float64(a)
	newMat = deepcopy(mat)
	newVec = deepcopy(vec)

	matMult = [k*a for k in newMat[i]]
	newMat[j] = map(add, newMat[j], matMult)

	vecMult = (newVec[i]) * a
	newVec[j] = newVec[j] + vecMult

	#for x in newMat:
	#	print x
	#print("\n\n")

	#for y in newVec:
	#	print y	

	return [newMat,newVec]	


def productAx(mat,vec):
	'''Returns product of full Matrix mat*vec = b'''
	mat = np.array(mat)
	vec = np.array(vec)
	b = mat.dot(vec)
	
	#for k in b:
	#	print k
	return b


#def rowPermuteCom(val,rowPtr,colInd,i,j):
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
	for ele in range(numRowI):
		rowIlist.append(val[rowIdx])
		colIlist.append(colInd[rowIdx])
		rowIdx = rowIdx + 1

	#add the 0s to rowIlist and their indexes
	for	i in range((len(rowPtr) - 1)):
		if i not in colIlist:
			colIlist.insert(i,i)
			rowIlist.insert(i,0)
	


	#GetrowJ elements and their indexes
	for elj in range(numRowJ):
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
	numNew = newrowPtr[(len(newrowPtr)) -1] - rowPtr[(len(rowPtr)) -1] 
	#print numNew
	#Update the values in val
	#print len(newRowJvals)
	#print newRowJvals
	#print valchangeIdx
	

	for newV in range((len(newRowJvals)) - numNew):
		newVal[valchangeIdx] = newRowJvals[newV]
		newColInd[valchangeIdx] = colJlist[(list(newRowJ)).index(newRowJvals[newV])]
		valchangeIdx = valchangeIdx + 1
	
	#print newV
	#print colJlist
	#print valchangeIdx
	if valchangeIdx != (rowPtr[(len(rowPtr)) -1]):
		#for v in range(numNew):
		#	missingVal = val[valchangeIdx - 1]
		#	missingIdx = colInd[valchangeIdx - 1]
		#newVal.insert(valchangeIdx,missingVal)
		#newColInd.insert(valchangeIdx,missingIdx)
		pass

	else:
		for v in range(numNew):
			newVal.insert(valchangeIdx,newRowJvals[newV + v + 1])
			#newColInd.insert(valchangeIdx,colJlist[newV + v + 1])
			newColInd.insert(valchangeIdx, (colJlist[(list(newRowJ)).index(newRowJvals[newV + v + 1])]))
			valchangeIdx = valchangeIdx + 1
	#print missingVal

	#newVal.insert(valchangeIdx,missingVal)
	#newColInd.insert(valchangeIdx,missingIdx)
	#print newColInd
	#print newVal
	#print newrowPtr
	#Scale Vector
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
			rowSum = rowSum + (val[value] * vec[colInd[value]])
			value = value + 1
			
		b.append(rowSum)
	
	
	return np.array(b)

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

	#print final
	return final

			 


rowPtr = [0,3,6,9,10,12]
colInd = [0,1,4,0,1,2,1,2,4,3,0,4]
val = [1,2,3,4,5,6,7,8,9,10,11,12]
vec = [5,4,3,2,1]
compMat = [val,rowPtr,colInd]
#B = (rowPermuteCom(compMat,vec,1,4))[0]
mat = retrieveElement(5,rowPtr,colInd,val)
#A = (rowPermute(mat,vec,1,4))[0]

#print(productAx(mat,vec))
#print(productAxComp(compMat,vec))
#tester(A,B)
A = (rowScale(mat,vec,1,4,3))[0]
#compMat = [val,rowPtr,colInd]
B = (rowScaleCom(compMat,vec,1,4,3))[0]


print tester(A,B)