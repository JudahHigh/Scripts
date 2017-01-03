#!/usr/bin/python

import os
import sys
import re

# reads in coordinates from a com file
# into matrix coordmat. Neglects reading
# atom information
def getcoords(fname,ftype):
	if (ftype=="com"):
		coordmat=[]
		nlcount=0
		inxyz=False
		with open(fname,'r') as pfile:
			for line in pfile:
				if (nlcount==3): # sig to stop reading coords
					inxyz=False
					break
				if (nlcount>=3): # sig to stop reading coords
					inxyz=False
				if inxyz:
					if (not "Tv" in line) and (line!='\n'):
						coordmat.append(line.strip().split()[1:len(line.strip().split())])
				if (nlcount==2) and (inxyz==False): # start reading at first xyzcoord
					inxyz=True
					continue
				if (line=='\n'): # iterate signal to read coords
					nlcount+=1
		return coordmat
	if (ftype=="xyz"):
		coordmat=[]
		with open(fname,'r') as pfile:
			for line in pfile:
				coordmat.append(line.strip().split()[1:len(line.strip().split())])
		return coordmat

# read in atom labels from com file
# violating DRY principle here for 
# readability and because I might be
# a little "tired"/lazy
def getatomlabels(fname,ftype):
	if (ftype=="com"):
		labels=[]
		nlcount=0
		inxyz=False
		with open(fname,'r') as pfile:
			for line in pfile:
				if inxyz:
					if (not "Tv" in line) and (line!='\n'):
						labels.append(line.strip().split()[0])
				if (nlcount==2) and (inxyz==False): # start reading at first label
					inxyz=True
					continue
				if (line=='\n'): # iterate signal to read labels
					nlcount+=1
				if (nlcount==3): # sig to stop reading coords
					break
		return labels
	if (ftype=="xyz"):
		labels=[]
		with open(fname,'r') as pfile:
			for line in pfile:
				labels.append(line.strip().split()[0])
		return labels

# for a general matrix (matrix mat of dimension d) 
# of literal strings try converting strings to 
# literal floats
def convMatStr2MatFloat(mat,d):
	if (d==0): # same as float(some data-type var)
		try:
			mat=float(mat)
		except ValueError:
			pass
		return mat
	if (d==1): # convert 1D vector of data-type vars to floats
		n=len(mat)
		for i in range(n):
			try:
				mat[i]=float(mat[i])
			except ValueError:
				pass
		return mat
	if (d==2): # convert 2D matrix of data-type vars to floats
		n=len(mat)
		m=len(mat[0][:])
		for i in range(n):
			for j in range(m):
				try:
					mat[i][j]=float(mat[i][j])
				except ValueError:
					pass
		return mat
	if (d==3): # convert 3D matrix of data-type vars to floats
		n=len(mat)
		m=len(mat[0][:])
		l=len(mat[0][0][:])
		for i in range(n):
			for j in range(m):
				for k in range(l):
					try:
						mat[i][j][k]=float(mat[i][j][k])
					except ValueError:
						pass
		return mat

def dumpcoords(labels,coords,case):
	if (case=="com"):
		prefix=getfname()
		outfile=open(prefix+'-trans.com','w')
		natoms=len(labels)
		# final sanity check
		if (natoms!=len(coords)):
			if verbose:
				sys.stderr.write("Something horrible has happend...\n  exiting...")
			sys.exit()
		elif (natoms==len(coords)):
			outfile.write('#p hf/sto-3g\n\ntitle\n\n0 1\n')
			for i in range(natoms):
				outfile.write("{:s}".format(labels[i]))
				for j in range(3):
					outfile.write("{: 13.8F}".format(coords[i][j]))
				outfile.write("\n")
			outfile.write("\n\n")
		else:
			sys.stderr.write("???\n  exiting...")
			sys.exit()
	if (case=="xyz"):
		prefix=getfname()
		outfile=open(prefix+'-trans.xyz','w')
		natoms=len(labels)
		# final sanity check
		if (natoms!=len(coords)):
			if verbose:
				sys.stderr.write("Something horrible has happend...\n  exiting...")
			sys.exit()
		elif (natoms==len(coords)):
			for i in range(natoms):
				outfile.write("{:s}".format(labels[i]))
				for j in range(3):
					outfile.write("{: 13.8F}".format(coords[i][j]))
				outfile.write("\n")
		else:
			sys.stderr.write("???\n  exiting...")
			sys.exit()
	if (case=="bind"):
		dumpbind(labels,coords,tv)

# generates generic name prefix from
# filename dilimeted by full stops '.'
def getfname():
	prefix=""
	for i in range(1,len(sys.argv)):
		if '.com' in sys.argv[i]:
			if (prefix!=""):
				prefix=prefix+"-"+sys.argv[i].strip().split('.com')[0]
			else:
				prefix=prefix+sys.argv[i].strip().split('.com')[0]
			break
	return prefix

def transCoords(coords,component,amount):
	for i in range(len(coords)):
		coords[i][component]=coords[i][component]+amount
	return coords

def getComponent(component):
	if (component=="x"):
		component=0
	elif (component=="y"):
		component=1
	elif (component=="z"):
		component=2
	else:
		component=0
	return component

# filename
fname=sys.argv[3]
# component to transform (x,y, or z)
component=sys.argv[1]
# amount of transform
amount=float(sys.argv[2])


coords=getcoords(sys.argv[3],"com")
labels=getatomlabels(sys.argv[3],"com")
coords=convMatStr2MatFloat(coords,2)
coords=transCoords(coords,getComponent(component),amount)
dumpcoords(labels,coords,"com")




