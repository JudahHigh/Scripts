#!/usr/bin/python
import os
import sys
import re
import numpy as np
import subprocess
from copy import deepcopy

def initialize(sysargv):
	# a dictionary of the atom information 
	# contained in the DinEMol data file
	# "my_eht_parameters.dat"
	# contains the possible orbital shells
	# included in the eht parameters for DinEMol
	eht={1:{'s':1,'label':'H'},2:{'s':1,'label':'He'},3:{'s':2,'p':2,'label':'Li'},4:{'s':2,'p':2,'label':'Be'},5:{'s':2,'p':2,'label':'B'},6:{'s':2,'p':2,'label':'C'},7:{'s':2,'p':2,'label':'N'},8:{'s':2,'p':2,'label':'O'},9:{'s':2,'p':2,'label':'F'},10:{'s':2,'p':2,'label':'Ne'},11:{'s':3,'p':3,'label':'Na'},12:{'s':3,'p':3,'label':'Mg'},13:{'s':3,'p':3,'label':'Al'},14:{'s':3,'p':3,'label':'Si'},15:{'s':3,'p':3,'label':'P'},16:{'s':3,'p':3,'label':'S'},17:{'s':3,'p':3,'label':'Cl'},18:{'s':3,'p':3,'label':'Ar'},19:{'s':4,'p':4,'label':'K'},20:{'s':4,'p':4,'d':3,'label':'Ca'},21:{'s':4,'p':4,'d':3,'label':'Sc'},22:{'s':4,'p':4,'d':3,'label':'Ti'},23:{'s':4,'p':4,'d':3,'label':'V'},24:{'s':4,'p':4,'d':3,'label':'Cr'},25:{'s':4,'p':4,'d':3,'label':'Mn'},26:{'s':4,'p':4,'d':3,'label':'Fe'},27:{'s':4,'p':4,'d':3,'label':'Co'},28:{'s':4,'p':4,'d':3,'label':'Ni'},29:{'s':4,'p':4,'d':3,'label':'Cu'},30:{'s':4,'p':4,'label':'Zn'},31:{'s':4,'p':4,'label':'Ga'},32:{'s':4,'p':4,'label':'Ge'},33:{'s':4,'p':4,'label':'As'},34:{'s':4,'p':4,'label':'Se'},35:{'s':4,'p':4,'label':'Br'},36:{'s':4,'p':4,'label':'Kr'},37:{'s':5,'p':5,'label':'Rb'},38:{'s':5,'p':5,'d':4,'label':'Sr'},39:{'s':5,'p':5,'d':4,'label':'Y'},40:{'s':5,'p':5,'d':4,'label':'Zr'},41:{'s':5,'p':5,'d':4,'label':'Nb'},42:{'s':5,'p':5,'d':4,'label':'Mo'},43:{'s':5,'p':5,'d':4,'label':'Tc'},44:{'s':5,'p':5,'d':4,'label':'Ru'},45:{'s':5,'p':5,'d':4,'label':'Rh'},46:{'s':5,'p':5,'d':4,'label':'Pd'},47:{'s':5,'p':5,'d':4,'label':'Ag'},48:{'s':5,'p':5,'d':4,'label':'Cd'},49:{'s':5,'p':5,'label':'In'},50:{'s':5,'p':5,'label':'Sn'},51:{'s':5,'p':5,'label':'Sb'},52:{'s':5,'p':5,'label':'Te'},53:{'s':5,'p':5,'label':'I'},54:{'s':5,'p':5,'label':'Xe'},55:{'s':6,'p':6,'label':'Cs'},56:{'s':6,'p':6,'d':5,'label':'Ba'},57:{'s':6,'p':6,'d':5,'label':'La'},58:{'s':6,'p':6,'d':5,'f':4,'label':'Ce'},59:{'s':6,'p':6,'d':5,'f':4,'label':'Pr'},60:{'s':6,'p':6,'d':5,'f':4,'label':'Nd'},61:{'s':6,'p':6,'d':5,'f':4,'label':'Pm'},62:{'s':6,'p':6,'d':5,'f':4,'label':'Sm'},63:{'s':6,'p':6,'d':5,'f':4,'label':'Eu'},64:{'s':6,'p':6,'d':5,'f':4,'label':'Gd'},65:{'s':6,'p':6,'d':5,'f':4,'label':'Tb'},66:{'s':6,'p':6,'d':5,'f':4,'label':'Dy'},67:{'s':6,'p':6,'d':5,'f':4,'label':'Ho'},68:{'s':6,'p':6,'d':5,'f':4,'label':'Er'},69:{'s':6,'p':6,'d':5,'f':4,'label':'Tm'},70:{'s':6,'p':6,'d':5,'f':4,'label':'Yb'},71:{'s':6,'p':6,'d':5,'f':4,'label':'Lu'},72:{'s':6,'p':6,'d':5,'label':'Hf'},73:{'s':6,'p':6,'d':5,'label':'Ta'},74:{'s':6,'p':6,'d':5,'label':'W'},75:{'s':6,'p':6,'d':5,'label':'Re'},76:{'s':6,'p':6,'d':5,'label':'Os'},77:{'s':6,'p':6,'d':5,'label':'Ir'},78:{'s':6,'p':6,'d':5,'label':'Pt'},79:{'s':6,'p':6,'d':5,'label':'Au'},80:{'s':6,'p':6,'d':5,'label':'Hg'},81:{'s':6,'p':6,'label':'Tl'},82:{'s':6,'p':6,'label':'Pb'},83:{'s':6,'p':6,'label':'Bi'},84:{'s':6,'p':6,'label':'Po'},85:{'s':6,'p':6,'label':'At'},86:{'s':6,'p':6,'label':'Rn'},87:{'s':7,'p':7,'label':'Fr'},88:{'s':7,'p':7,'label':'Ra'},89:{'s':7,'p':7,'d':6,'label':'Ac'},'$$':{'s':1,'p':1,'label':''}}

	# only argument for script
	# formatted g09 checkpoint
	# file and mo numbers
	fchk=sysargv[1]
	molist=sysargv[2:len(sysargv)]
	nmo=len(molist)
	monum=18

	# hardcoded boolean to print
	# debugging information
	debugmode=False

	# Greps out relevant information into variables from fchk file
	nshtyp=int(cmd(['grep','Shell types',fchk]).strip().split()[len(cmd(['grep','Shell types',fchk]).strip().split())-1]) # number of shell type elements
	nshatm=int(cmd(['grep','Shell to atom map',fchk]).strip().split()[len(cmd(['grep','Shell to atom map',fchk]).strip().split())-1]) # number of shell to atom map elements
	nenerg=int(cmd(['grep','Alpha Orbital Energies',fchk]).strip().split()[len(cmd(['grep','Alpha Orbital Energies',fchk]).strip().split())-1]) # number of energies or MOs or AOs
	ncoeff=int(cmd(['grep','Alpha MO coefficients',fchk]).strip().split()[len(cmd(['grep','Alpha MO coefficients',fchk]).strip().split())-1]) # number of MO coefficients
	nbasis=int(cmd(['grep','Number of basis functions',fchk]).strip().split()[len(cmd(['grep','Number of basis functions',fchk]).strip().split())-1]) # number of basis functions
	nelec=int(cmd(['grep','Number of electrons',fchk]).strip().split()[len(cmd(['grep','Number of electrons',fchk]).strip().split())-1]) # number of electrons
	natnum=int(cmd(['grep','Atomic numbers',fchk]).strip().split()[len(cmd(['grep','Atomic numbers',fchk]).strip().split())-1]) # number of Atomic Number elements
	natoms=natnum # number of atoms

	shtyp=remJunk(cmd(['grep','-A',str(numlines(nshtyp,6)),'Shell types',fchk]).strip().split()) # stores elements of shell type section
	shatm=remJunk(cmd(['grep','-A',str(numlines(nshatm,6)),'Shell to atom map',fchk]).strip().split()) # stores elements of shell to atom map section
	coeff=remJunk(cmd(['grep','-A',str(numlines(ncoeff,5)),'Alpha MO coefficients',fchk]).strip().split()) # stores elements of coefficient matrix
	atnum=remJunk(cmd(['grep','-A',str(numlines(natnum,6)),'Atomic numbers',fchk]).strip().split()) # stores elements of atomic number section

	return eht,debugmode,molist,nmo,fchk,monum,nshtyp,nshatm,nenerg,ncoeff,nbasis,nelec,natnum,natoms,shtyp,shatm,coeff,atnum


# this is a general function for
# carrying out a system (BASH) cmd
# where the output is returned.
# the input a is a list of the command
# and arguments.
def cmd(a):
	proc = subprocess.Popen(a,stdout=subprocess.PIPE)
	stdout,stderr=proc.communicate()
	return stdout

# determines the number of lines
# containing relevant data
# after a matched header line
# in the formatted checkpoint file
# in which the header contains
# the number (num) of data
# elements. Case corresponds to
# the number of data elements
# within each line which is 
# specific to the type of data
# contained
def numlines(num,case):
	if case==6:
		if num%6!=0:
			nlines=num/6+1
			return nlines
		else:
			nlines=num/6
			return nlines
	if case==5:
		if num%5!=0:
			nlines=num/5+1
			return nlines
		else:
			nlines=num/5
			return nlines

# after a section of the fchk file is
# copied to list a, header lines and 
# irrelevant data is removed from
# the list by remJunk
def remJunk(a):
	b=deepcopy(a)
	for i in range(len(a)):
		try:
			float(a[i])
		except ValueError:
			b.remove(a[i])
	b.pop(0)
	return b

# In the loop determining the maximum shell for a
# given atom in the g09 fchk file, this function is
# called to determine whether or not a given AO within
# a shell should be included on the basis that it is 
# parametrized by the eht theory in DinEMol... hints
# the name truDinn or "try DinEMol n"
def tryDinn(i,curn,ang,atnum,shatm,eht,correction):
	try:
		dinn=eht[int(atnum[int(shatm[i])-1])][ang]
		if dinn-(correction)==0:
			return 1
		else:
			return 0
	except KeyError:
		return 0


# The inherent order of p and d basis functions
# used by G09 for a given atom is different than 
# the convention used by DinEMol. Therefore we must
# take care to rearrange the coefficients extracted 
# from the G09 fchk file such they are in the order
# demanded by DinEMol. The basis function ordering
# in DinEMol and G09 for sp, p and d shells is as
# follows
# Din p=[y,z,x]
# Din d=[xy,yz,z2,xz,x2y2]
# yaemop d =[x2y2,z2,xy,xz,yz]
# G09 p=[x,y,z]
# G09 d=[z2,xz,yz,x2y2,xy]
def getnewind(i,shell,place):
	adjspind={0:0,1:1,2:1,3:-2}
	adjpind={0:1,1:1,2:-2}
	# d-dcit for g09-->dinemol
	adjdind={0:4,1:1,2:-2,3:-2,4:-1}
	# d-dcit for g09-->yaemop
	if shell==0:
		return i,place
	if shell==-1:
		if place==4:
			place=0
		correction=adjspind[place]
		iold=i
		i=i+correction
		return i,place
	if shell==1:
		if place==3:
			place=0
		correction=adjpind[place]
		i=i+correction
		return i,place
	if shell==-2:
		if place==5:
			place=0
		correction=adjdind[place]
		i=i+correction
		return i,place

# this function is necessary for modifying indices
# when parsing through the shell to atom map and 
# shell type sections of the fchk file, such that
# the shells are read correctly from shell to shell
# without incorrectly counting two subsequent
# sp shells as a single shell or two subsequent
# d shells as a single d shell. Sort of abstract function.
def setangcount(currshell,angcount):
	if (currshell==-1 and angcount==4):
		angcount=0
		return angcount
	if (currshell==-2 and angcount==5):
		angcount=0
		return angcount
	else:
		return angcount

def newbasisnum(x):
	n=0
	for i in range(len(x)):
		if x[i]!=0:
			n+=1
	return n

# maxn is an array that contains the max
# n for any atom in the fchk file. max n
# really only depends on the number of
# s, p or sp shells, not on d or f shells.
# however f shells are neglected as DinEMol
# cannot use atoms with them yet and no 
# sto-3g basis functions are defined for 
# f-type orbitals
def getmaxn(maxn,natoms,nshtyp,shtyp,shatm):
	n=0
	curatm=1
	for i in range(nshtyp):
		if int(shatm[i])!=curatm:
			curatm=int(shatm[i])
			n=0
		if (int(shtyp[i])==0 or int(shtyp[i])==-1):
			n+=1
			maxn[curatm-1]=n
		if (int(shtyp[i])==-2 or int(shtyp[i])==2):
			pass
	return maxn

# x is an array that determines if a given
# shell (one/multiple basis functions) is included or removed going
# from G09 to DinEMol. This is the key to removing core electrons 
# as is done in eht which only includes a valence description of 
# many-electron systems. If a shell is included, x[i]==1, if not
# x[i]==0
def getxandpr(nshtyp,shatm,atnum,eht,x,pr,maxn):
	curn=0
	curatm=1
	curd=3
	for i in range(nshtyp):
		if (int(shatm[i])!=curatm):
			curatm=int(shatm[i])
			curn=0
			curd=3
		n=maxn[int(shatm[i])-1]
		curn+=1
		if curn<n:# handles non-valence shells (s,p or sp)
			x[i]=0
			pr[i]=curn# handles valence shells (s,p or sp)
		if curn==n:
			x[i]=1
			pr[i]=curn
		if curn>n:# handles shells with greater l
			if (int(shtyp[i])==-2 or int(shtyp[i])==2):
				x[i]=tryDinn(i,curn,'d',atnum,shatm,eht,curd)
				pr[i]=curd
				curd+=1
	return x,pr

# algorithm for extending arrays from shell convention
# to basis function convention
# "shellformats" is a dictionary that contains number
# of basis functions for a given G09 shell type
def extendarrays(nshtyp,shtyp,shatm,atnum,x,pr,shtypprime,shatmprime,xprime,prprime,atnumprime):
	shellformats={0:1,1:3,-1:4,2:6,-2:5,3:10,-3:7}
	curind=-1
	for i in range(nshtyp):
		for j in range(shellformats[int(shtyp[i])]):
			curind+=1
			shtypprime[curind]=int(shtyp[i])
			shatmprime[curind]=int(shatm[i])
			xprime[curind]=x[i]
			prprime[curind]=pr[i]
			atnumprime[curind]=atnum[int(shatm[i])-1]
	return shtypprime,shatmprime,xprime,prprime,atnumprime


# creates a reordered matrix containing indices necessary
# to rearrange MO coefficients such that the p and d shell
# basis functions reflect the ordering in DinEMol.
def makereorder(reorder,nbasis,shtypprime,shatmprime):
	currsh=4
	curratom=-1
	for i in range(nbasis):
		if (shtypprime[i]!=currsh or shatmprime[i]!=curratom):
			currsh=shtypprime[i]
			curratom=int(shatmprime[i])
			place=0
		adjind,place=getnewind(i,shtypprime[i],place)
		reorder[i]=adjind
		place+=1
	return reorder

# Prints debugging information to stdout to determine if the script has
# done its job. can be commented
def debugout(debugmode,xprime,shtypprime,shatmprime,atnumprime,eht,prprime,monum,coeff,nbasis,reorder):
	if debugmode:
		angtypes={0:{0:'   s'},-1:{0:'   s',1:'  py',2:'  pz',3:'  px'},1:{0:'  py',1:'  pz',2:'  px'},-2:{0:'  xy',1:'  yz',2:'  z2',3:'  xz',4:'x2y2'}}
		present={0:'N',1:'Y'}
		angcount=-1
		currshell=-500
		curratom=-1
		sys.stdout.write("#    Atom-# Atom n ang i j coefficient keep?\n")
		for i in range(len(xprime)):
			if (shtypprime[i]!=currshell or shatmprime[i]!=curratom):
				currshell=int(shtypprime[i])
				curratom=int(shatmprime[i])
				angcount=0
			angcount=setangcount(currshell,angcount)
			sys.stdout.write(" {:5d}  {!s} {:2d} {:2d} {!s} {:5d} {:5d} {: 16.8E} {!s}\n".format(int(atnumprime[i]),eht[atnumprime[i]]['label'],int(prprime[i]),int(shtypprime[i]),angtypes[currshell][angcount],i+1,monum,float(coeff[((monum-1)*nbasis)+int(reorder[i])]),present[xprime[i]]))
			angcount+=1

# puts new index values into xprime to 
# make xprime a cipher between STO-6G
# and STO at EHT level
def replzerosxprime(xprime,reorder):
	for i in range(len(xprime)):
		if xprime[i]==1:
			xprime[i]=reorder[i]
		if xprime[i]==0:
			xprime[i]=-1
	return xprime

# creates a dictionary that translates
# indices in n-basis to those over
# a reduced basis size m-basis such
# that indices for core basis functions
# are ignored
def makexdict(xprime):
	xdict={}
	j=-1
	for i in range(len(xprime)):
		if xprime[i]!=-1:
			j=j+1
			xdict[xprime[i]]=j
		else:
			xdict[i]=-1
	return xdict

# prepares a new set of coefficients (cnu)
# in the reduced basis, m-basis, that 
# lacks core basis functions
def makecnu(cnu,nmo,molist,mbasis,nbasis,xprime,coeff,xdict):
	nmdiff=nbasis-mbasis
	cnu[:,:]=-1
	coeff=np.reshape(coeff,(nbasis,nbasis),'F')
	for i in range(nmo):
		cmo=int(molist[i].split('-')[0])-1
		cnumo=int(molist[i].split('-')[1])-1
		for j in range(nbasis):
			if xdict[j]!=-1:
				cnu[cnumo,xdict[j]]=coeff[j,cmo]
	return cnu

# simply prints to file the reduced
# basis coefficients in cnu in fortran
# indices
def writedata(mbasis,cnu):
	nocoreout=open('cnocore.dat','w')
	for i in range(mbasis):
		for j in range(mbasis):
			if cnu[i,j]!=-1:
				nocoreout.write("{:3d} {:3d} {: 16.8E}\n".format(i+1,j+1,cnu[i,j]))
	nocoreout.close()

########
#script#
########
def main(sysargv):
	eht,debugmode,molist,nmo,fchk,monum,nshtyp,nshatm,nenerg,ncoeff,nbasis,nelec,natnum,natoms,shtyp,shatm,coeff,atnum=initialize(sysargv)

	maxn=np.zeros(natoms)
	maxn=getmaxn(maxn,natoms,nshtyp,shtyp,shatm)

	x=np.zeros(nshtyp)
	pr=np.zeros(nshtyp)
	x,pr=getxandpr(nshtyp,shatm,atnum,eht,x,pr,maxn)

	# intiializes extended arrays for shell types, shell
	# to atom map, x, princpal quantum number, and atomic 
	# number.
	# this is necessary to move from the shell convention to
	# a basis function convention
	shtypprime=np.zeros(nbasis)
	shatmprime=np.zeros(nbasis)
	xprime=np.zeros(nbasis)
	prprime=np.zeros(nbasis)
	atnumprime=np.zeros(nbasis)
	shtypprime,shatmprime,xprime,prprime,atnumprime=extendarrays(nshtyp,shtyp,shatm,atnum,x,pr,shtypprime,shatmprime,xprime,prprime,atnumprime)

	reorder=np.zeros(nbasis)
	reorder=makereorder(reorder,nbasis,shtypprime,shatmprime)

	debugout(debugmode,xprime,shtypprime,shatmprime,atnumprime,eht,prprime,monum,coeff,nbasis,reorder)

	xprime=replzerosxprime(xprime,reorder)

	xdict=makexdict(xprime)

	mbasis=newbasisnum(xprime)
	cnu=np.zeros((mbasis,mbasis))
	cnu=makecnu(cnu,nmo,molist,mbasis,nbasis,xprime,coeff,xdict)
	
	writedata(mbasis,cnu)

main(sys.argv)
		

