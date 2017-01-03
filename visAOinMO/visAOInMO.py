#!/usr/bin/python
import os
import sys
import numpy as np
import re
from time import time as t
from copy import deepcopy
import linecache

#######################################################
#  sys.argv[1] == .fchk file to be read					#
#  sys.argv[2] == MO to be collapsed						#
#  sys.argv[3] == alpha or beta MO							#
#  sys.argv[4] == AO that MO will be collapsed onto  	#
#																		#
#  					:: Example input ::						#
#  		python script.py file.fchk 239 a p				#
#######################################################

# Simple function for converting strings to integers
# or floats.
def convertStr(s):
	try:
		ret = int(s)
	except ValueError:
		ret = float(s)
	return ret

# Returns the number of basis functions in fchk file
def get_nbasis(filename):
	nbasis=0
	fchk=open(filename,'r')
	fchkline=fchk.readline()
	while fchkline:
		if 'Number of basis functions' in fchkline:
			return convertStr(fchkline.strip().split()[len(fchkline.strip().split())-1])
			break
		fchkline=fchk.readline()
	fchk.close()

def get_shelltypes(filename):
	shelltypes=[]
	numitems=0
	start=False
	fchk=open(filename,'r')
	fchkline=fchk.readline()
	while fchkline:
		if start and len(shelltypes)<=numitems:
			for i in range(len(fchkline.strip().split())):
				shelltypes.append(convertStr(fchkline.strip().split()[i]))
		if start and len(shelltypes)==numitems:
			return shelltypes
			break
		if 'Shell types' in fchkline:
			numitems=convertStr(fchkline.strip().split()[len(fchkline.strip().split())-1])
			start=True
		fchkline=fchk.readline()
	fchk.close()

def get_shellatommap(filename):
	shatmap=[]
	numitems=0
	start=False
	fchk=open(filename,'r')
	fchkline=fchk.readline()
	while fchkline:
		if start and len(shatmap)<=numitems:
			for i in range(len(fchkline.strip().split())):
				shatmap.append(convertStr(fchkline.strip().split()[i]))
		if start and len(shatmap)==numitems:
			return shatmap
			break
		if 'Shell to atom map' in fchkline:
			numitems=convertStr(fchkline.strip().split()[len(fchkline.strip().split())-1])
			start=True
		fchkline=fchk.readline()
	fchk.close()	

def AorB(arg):
	ab=''
	if arg=='a':
		ab='Alpha'
		return ab
	elif arg=='b':
		ab='Beta'
		return ab

def get_MOcoef(filename,nb,MO,ab):
	numcoef=0
	MObn=nb*(convertStr(MO)-1)+1
	MOen=nb*(convertStr(MO)-1)+nb
	MOcoef=[]
	findMO=False
	getMOcoef=False
	fchk=open(filename,'r')
	fchkline=fchk.readline()
	while fchkline:
		if findMO:
			for i in range(len(fchkline.strip().split())):
				numcoef+=1
				if numcoef==MObn:
					getMOcoef=True
				if getMOcoef and len(MOcoef)<=nb:
					MOcoef.append(convertStr(fchkline.strip().split()[i]))
				if len(MOcoef)==nb:
					return MOcoef
					break	
		if ab+' MO coefficients' in fchkline:
			findMO=True
		fchkline=fchk.readline()
	return MOcoef

def put_MOcoef(filename,nb,MO,ab,MOcoef):
	newfchk=open(filename.strip().split('.')[0]+'New.fchk','w')
	oldfchk=open(filename,'r')
	allc=np.zeros(nb*nb,dtype=np.float_)
	MO=convertStr(MO)
	for i, line in enumerate(oldfchk, 1):
		if ab+' MO coefficients' in line:
			bi=i
			nc=convertStr(line.strip().split()[len(line.strip().split())-1])
			if nc%5!=0:
				nclines=(nc/5)+1
			if nc%5==0:
				nclines=(nc/5)
			ei=bi+nclines
	for i in range(ei-bi):
		for j in range(len(linecache.getline(filename,(bi+1)+i).strip().split())):
			allc[(i*5)+j]=linecache.getline(filename,(bi+1)+i).strip().split()[j]
	mobi=(MO*nb)-nb
	moei=(MO*nb)
	allc[mobi:moei]=MOcoef[0:len(MOcoef)]
	oldfchk.close()
	oldfchk=open(filename,'r')
	for i, line in enumerate(oldfchk,1):
		if ab+' MO coefficients' in line:
			newfchk.write(line)
			break
		if not ab+' MO coefficients' in line:
			newfchk.write(line)
	r=allc%5
	for i in range(len(allc)/5):
		newfchk.write(' {: 13.8E} {: 13.8E} {: 13.8E} {: 13.8E} {: 13.8E}\n'.format(allc[i*5],allc[(i*5)+1],allc[(i*5)+2],allc[(i*5)+3],allc[(i*5)+4]))
	for i in range(len(allc)%5):
		newfchk.write(' {: 13.8E} '.format(allc[len(allc)-(len(allc)%5)+i]))
	newfchk.write('\n')
	newfchk.close()
		



def collapseMOcoef(MOcoef,shelltypes,shatmap,AO):
	bfls=[]
	for i in range(len(shelltypes)):
		if shelltypes[i]==0:
			bfls.append('s')
		if shelltypes[i]==-1:
			bfls.append('s')
			bfls.append('x')
			bfls.append('y')
			bfls.append('z')
		if shelltypes[i]==-2:
			bfls.append('3ZZ-RR')
			bfls.append('XZ')
			bfls.append('YZ')
			bfls.append('XX-YY')
			bfls.append('XY')
	for i in range(len(bfls)):
		if AO!='p' and AO!='d' and AO!='f':
			if bfls[i]!=AO:
				MOcoef[i]=0.0
		if AO.strip()=='p':
			if bfls[i]=='x' or bfls[i]=='y' or bfls[i]=='z':
				pass
			elif bfls[i]!='x' and bfls[i]!='y' and bfls[i]!='z':
				MOcoef[i]=0.0
		if AO.strip()=='d':
			if bfls[i]=='3ZZ-RR' or bfls[i]=='XZ' or bfls[i]=='YZ' or bfls[i]=='XX-YY' or bfls[i]=='XY':
				pass
			elif bfls[i]!='3ZZ-RR' and bfls[i]!='XZ' and bfls[i]!='YZ' and bfls[i]!='XX-YY' and bfls[i]!='XY':
				MOcoef[i]=0.0
	return MOcoef

t1=t()
MOcoeflist=collapseMOcoef((get_MOcoef(sys.argv[1],get_nbasis(sys.argv[1]),sys.argv[2],sys.argv[3])),\
		get_shelltypes(sys.argv[1]),get_shellatommap(sys.argv[1]),sys.argv[4])
put_MOcoef(sys.argv[1],get_nbasis(sys.argv[1]),sys.argv[2],sys.argv[3],MOcoeflist)
t2=t()
print 'TIME :: ',t2-t1

