#!/usr/bin/python

import os
import sys
import re
import math

# this script takes in a xyz coordinate file in 
# angstroms along with the cyrstollagraphic unit cell
# dimensions (a, b, c) and parameters (alpha, beta, gamma)
# and returns a file with fractional coordinates

# A conversion matrix is necessary to perform this function
# on a 1D xyz vector. The conversion matrix in cartesian coordinates
# is of the form,
#
# { 1/a -cos(gamma)/a*sin(gamma) cos(alpha)*cos(gamma)-cos(beta)/a*v*sin(gamma) ,
#    0       1/b*sin(gamma)      cos(beta)*cos(gamma)-cos(alpha)/b*v*sin(gamma) ,
#    0             0                              sin(gamma)/c*v                }
#
# where v = [ 1 - cos(alpha)**2 - cos(beta)**2 - cos(gamma)**2 + 2*cos(alpha)*cos(beta)*cos(gamma) ]**0.5
#
# Each xyz vector to be matrix multiplied to the transformation matrix is of the form
#
#                            { x , y, z }
#
# Keep in mind that this script is a redone and upgraded version of the bash script
# also written by me called ietingen.sh

#####################################################################################
######################### START USER PARAMETER SETTINGS #############################
#####################################################################################

# input file types for adsorbate and slab ( "com" or "xyz" only )
ftype="xyz"

# output type desired ("xyz","com","bind")
outtype="bind"

# print all information?
verbose=False

# default lattice vecs
a=30.49498400 # lattice vec a
b=31.46113821 # lattice vec b
c=45.00000000 # lattice vec c
tv=[a,b,c]

# time step [fs] and total time of simulation [fs]
tstp=0.1
nfms=100

# what is charge of the system
chrg=0

# initial orbitals and weight
iorb="149"
ci="0.7141737480250215"
jorb="150"
cj="0.6999684690269221"

# adsorbate coordinate parameters
# use get_matching_atom_numbers.py to
# get atom_ranges_ads_string
# and atom_ranges_slab_string
natms_ads=108 # number of adsorbate atoms
atom_ranges_ads_string="865-972"

natms_slab=864 # number of slab atoms
atom_ranges_slab_string="1-864"

# generate cubes or not
# type Cube (true) or leave blank (false)
cubes="Cube"

# absorbing atom ranges
# separate numbers (inclusive ranges) by "-" 
# and if multiple ranges use comma "," dilimeter
# HINT: use the get_matching_atom_numbers.py script
# Judah wrote to get a range of atoms to put here
absorbing_atoms="1-288"

# do pDOS ?"
do_pdos=True

# custom parameters?
# user needs to make custom_parameters.dat
custom_params=True

#####################################################################################
########################## END USER PARAMETER SETTINGS ##############################
#####################################################################################

# define the dict used by IETSim which specifies the number of basis functions for any given atom
# these numbers may vary for certain atoms in different implemtations of EHT, but this dict is exactly
# what is specified for use in IETSim and IETSim only.
basis = { "BE" : 4, "BA" : 9, "BI" : 4, "BK" : 23, "BR" : 4, "RU" : 9, "RE" : 9, "LU" : 23, "RA" : 4, "RB" : 4, "RN" : 4, "RH" : 9, "H" : 1, "P" : 4, "GE" : 4, "GD" : 23, "GA" : 4, "OS" : 9, "C" : 4, "HO" : 23, "HF" : 9, "HG" : 9, "HE" : 1, "PR" : 23, "PT" : 9, "PU" : 23, "PB" : 4, "PA" : 23, "PD" : 9, "PO" : 4, "PM" : 23, "ZN" : 4, ";CR" : 9, "K" : 4, "O" : 4, ";CE" : 23, "S" : 4, "W" : 9, "EU" : 23, "ZR" : 9, "ER" : 23, "MD" : 23, "MG" : 4, "MO" : 9, "MN" : 9, "U" : 23, "FR" : 4, "FE" : 9, "FM" : 23, "NI" : 9, "NO" : 23, "NA" : 4, "NB" : 9, "ND" : 23, "NE" : 4, "ES" : 23, "NP" : 23, "UNQ" : 23, "B" : 4, "CO" : 9, "CM" : 23, "CL" : 4, "CA" : 9, "CF" : 23, "CE" : 23, "N" : 4, "V" : 9, "CS" : 4, "CR" : 9, "CU" : 9, ";TI" : 9, "SR" : 9, "KR" : 4, "SI" : 4, "SN" : 4, "SM" : 23, "SC" : 9, "SB" : 4, "SE" : 4, "YB" : 23, "DY" : 23, "LA" : 9, "F" : 4, "LI" : 4, "TL" : 4, "TM" : 23, "LR" : 23, "TH" : 23, "TI" : 9, "TE" : 4, "TB" : 23, "TC" : 9, "TA" : 9, "AC" : 9, "AG" : 9, "I" : 4, "IR" : 9, "AM" : 23, "AL" : 9, "AS" : 4, "AR" : 4, "AU" : 9, "AT" : 4, "IN" : 4, "Y" : 9, "CD" : 9, "XE" : 4,  }

def gen_abs_atoms_list(abs_atom_range):
	abs_atoms = []
	range_list = abs_atom_range.split(',')
	for i in range(len(range_list)):
		if ("-" in range_list[i]):
			temp_list = range_list[i].split("-")
			for j in range(int(temp_list[0]),int(temp_list[1])+1):
				abs_atoms.append(j)
		elif (not "-" in range_list[i]):
			abs_atoms.append(range_list[i])
	return abs_atoms

def gen_basis_num_list(labels,basis,abs_atom_range):
	abs_atoms = gen_abs_atoms_list(abs_atom_range)
	nums=[]
	for i in abs_atoms:
		atom_num = i
		nums += basis_numbers(atom_num,labels,basis)
	abs_string = gen_abs_string(nums)
	return abs_string

def basis_numbers(atom_num,labels,basis):
	b_nums = []
	num_start = 0
	for i in range(atom_num-1):
		num_start += basis[labels[i].upper()]
	for i in range(1,basis[labels[atom_num-1].upper()]+1):
		b_nums.append(num_start+i)
	return b_nums

def gen_abs_string(nums):
	outline = ''
	outline += 'Absorbing\n'
	outline += '{:d} {: 4.3f}\n'.format(len(nums),0.1)
	for i in range(len(nums)):
		if i%10==9:
			outline += '{:d}   \\\n'.format(nums[i])
		elif i==len(nums)-1:
			outline += '{:d}\n'.format(nums[i])
		else:
			outline += '{:d}, '.format(nums[i])
	return outline

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
				if inxyz:
					if (not "Tv" in line) and (line!='\n'):
						coordmat.append(line.strip().split()[1:len(line.strip().split())])
				if (nlcount==2): # start reading at first xyzcoord
					inxyz=True
					continue
				if (line=='\n'): # iterate signal to read coords
					nlcount+=1
				if (nlcount==3): # sig to stop reading coords
					break
		return coordmat
	if (ftype=="xyz"):
		coordmat=[]
		skip_header_count=0
		with open(fname,'r') as pfile:
			for line in pfile:
				skip_header_count+=1
				if (skip_header_count > 2):
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
				if (nlcount==2): # start reading at first label
					inxyz=True
					continue
				if (line=='\n'): # iterate signal to read labels
					nlcount+=1
				if (nlcount==3): # sig to stop reading coords
					break
		return labels
	if (ftype=="xyz"):
		labels=[]
		skip_header_count=0
		with open(fname,'r') as pfile:
			for line in pfile:
				skip_header_count+=1
				if (skip_header_count > 2):
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

# parse through coordinates to get lattice vectors
# a, b and c stored in 1D vec tv
# assumes alpha, beta and gamma are 90 although this is
# generally not the case. Functionality to calc alpha,
# beta and gamma from a, b and c to be added later.
def gettv(comfile):
	global tv
	temptv=[]
	i=1
	FOUND=False
	with open(comfile,'r') as pfile:
		for line in pfile:
			if "Tv" in line:
				if (i==3):
					FOUND=True
				temptv.append(line.strip().split()[i])
				i+=1
	if FOUND:
		tv=temptv # found Tvs in comfile and will use
	if not (FOUND):
		if verbose:
			sys.stderr.write("no Tvs found in "+sys.argv[1]+", used default ["+str(tv[0])+","+str(tv[1])+","+str(tv[2])+"]")
	return tv

# constructs the coordinate transformation matrix
# to be used to tranform cartesian coordinates to
# to fractional coordinates
def maketmat(tv,case):
	if (case==0): # what wikipedia does 
		a=tv[0]
		b=tv[1]
		c=tv[2]
		al=be=ga=90.0
	
		# initializes 3x3 tranformation matrix 
		tmat=[ [ 0 for i in range(3) ] for j in range(3) ]
	
		# calculate elements of transformation matrix as
		# prescribed by https://en.wikipedia.org/wiki/Fractional_coordinates
	
		v=(1.0-(math.cos(al)**2.0)-(math.cos(be)**2.0)-(math.cos(ga)**2.0)+(2.0*math.cos(al)*math.cos(be)*math.cos(ga)))**0.5
	
		tmat[0][0]=1.0/a
		tmat[1][0]=0.0
		tmat[2][0]=0.0
		tmat[0][1]=(-1*((math.cos(ga))/(a*math.sin(ga))))
		tmat[1][1]=1.0/(b*math.sin(ga))
		tmat[2][1]=0.0
		tmat[0][2]=((math.cos(al)*math.cos(ga))-math.cos(be))/(a*v*math.sin(ga))
		tmat[1][2]=((math.cos(be)*math.cos(ga))-math.cos(al))/(a*v*math.sin(ga))
		tmat[2][2]=math.sin(ga)/(c*v)

		return tmat
	if (case==1): # what Batista's com_to_crystbind.py does
		tmat=[ [ 0 for i in range(3) ] for j in range(3) ]
		for i in range(3):
			tmat[i][i]=1.0/tv[i]
		return tmat


# using preconstucted transformation matrix
# and a coordinate matrix, converts all
# coordinates to fractional
def transform(coords,tmat):
	for i in range(len(coords)):
		cvec=coords[i]
		tvec=[0.0,0.0,0.0]
		# loop matrix multiply T*C = V (T = tmat, C = cvec, V = tvec)
		for j in range(3):
			for k in range(3):
				tvec[j]=tvec[j]+tmat[j][k]*cvec[k] # perform transform element by element
		coords[i]=tvec
	return coords

# dumps the labels along with their fractional 
# coordinates and original translation vectors 
# to new file to be fed into Judah's bash script
# for constructing ietsim input file.
#
# again ignoring DRY principle here because I
# am lazy and need to get things done ;)
def dumpfraccoords(labels,coords,tv,case,basis_num_list="",param_dict={}):
	if (case=="com"):
		prefix=getfname()
		outfile=open(prefix+'.com','w')
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
		outfile=open(prefix+'.xyz','w')
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
		dumpbind(labels,coords,tv,basis_num_list,param_dict)

# dumps to bind format for ietsim
def dumpbind(labels,coords,tv,basis_num_list="",param_dict={}):
	natms=len(labels)
	prefix=getfname()
	outfile=open(prefix+'.bind','w')
	outfile.write(prefix+'.bind\n\n')
	outfile.write('Geometry Crystallographic\n')
	outfile.write("{:d}\n".format(natms+3))
	for i in range(natms):
		if ( not i+1 in param_dict.keys() ): # if no custom parameter
			outfile.write("{:3d}  {:2s}".format(i+1,labels[i]))
		elif ( i+1 in param_dict.keys() ): # custom parameter exists :[]
			outfile.write("{:3d}  * ".format(i+1))
		for j in range(3):
			outfile.write("  {:9.6F}".format(coords[i][j]))
		outfile.write("\n")
	uvec=[[coords[0][0]+1,coords[0][1],coords[0][2]],[coords[0][0],coords[0][1]+1,coords[0][2]],[coords[0][0],coords[0][1],coords[0][2]+1]]
	for i in range(3):
		outfile.write("{:3d}  {:2s}".format(natms+i+1,'&'))
		for j in range(3):
			outfile.write("  {:9.6F}".format(uvec[i][j]))
		outfile.write("\n")
	outfile.write("\nParameters\n")
	for i in range(natms):
		if ( (i+1) in param_dict.keys() ):
			outfile.write(param_dict[i+1]+"\n")
	outfile.write("\nCharge\n{:d}\n\n".format(chrg))
	outfile.write("Lattice\n3\n1 1 1\n1 {:d}\n1 {:d}\n1 {:d}\n\n\n".format(natms+1,natms+2,natms+3))
	outfile.write("Crystal Spec\n{:F}  {:F}  {:F}\n90  90  90\n\n".format(tv[0],tv[1],tv[2]))
	outfile.write("Average Properties")
	outfile.write("{:s}".format(gen_pDOS_string()))
	outfile.write("\n\nkpoints\n1\n0.000000  0.000000  0.000000 1\n\n")
	outfile.write("Dynamics\n{:2.1F} {:3.1F}\n\n".format(tstp,nfms))
	temp = format_atom_range_string(atom_ranges_ads_string)
	outfile.write("Adsorbate\n{:d} {:s} {:s} {:s} {:s}\n{:s}\n\n".format(natma,iorb,ci,jorb,cj,format_atom_range_string(atom_ranges_ads_string)))
	outfile.write("Occupation\n{:d}\n{:s}\n\n".format(natmb,format_atom_range_string(atom_ranges_slab_string)))
	outfile.write("{:s}\n\n".format(cubes))
	outfile.write(basis_num_list)
	outfile.write("\n\n")

# Extensive IETsim test calculations wer done in
# order to determine the features of the .bind files
# that must absolutely be prepared in a certain manner.
# Both the "Absorbate" and "Occupation" sections must 
# include atom range strings that define the atoms in
# the extended system comprising the adsorbate and the
# portion of the system to compute survival probabilities
# over respectively.
#
# One might mistakingly write one of these atom ranges 
# as "1-864". This will not cause the program to crash,
# however it will cause very large and strange P(t) values,
# in my test cases on the order of 600000! The way the atom
# range MUST be formatted to prevent this unfortunate problem
# is to reformat "1-864" to "1,2-864".
#
# This reformatting is
# precisely what this function does. If given "1-864", the
# function will return the string "1,2-864" which will be
# inserted later into its respective place in the input file.
# If given "1,2-864" the function will simply return the input
# string "1,2-864". Simple yet absolutely necessary.
#
# It is subtle formatting issues like this that cause research
# and progress to come to a streaking halt and should not be
# experienced in the first place :)
def format_atom_range_string(atom_range_string):
	temp = atom_range_string.split(',')
	if ( '-' in temp[0] ):
		left = temp[0].split('-')[0]
		right = temp[0].split('-')[1]
		new_string = left+','+str(int(left)+1)+'-'+right
		temp[0] = new_string
		final_string = ','.join(temp)
		return final_string
	else:
		return atom_range_string
	

# generates the projected density of states
# section for the input file
# calls on another function which makes the atom
# number lines in the correct format that are
# required. Assumes the user wants to do a pDOS
# for the dye(1) and slab(2)
def gen_pDOS_string():
	pDOS_string=""
	if do_pdos:
		pDOS_string = "\n\nProjected DOS\n2\n"
		dye_string = general_dos_string_generator(atom_ranges_ads_string)
		pDOS_string += dye_string+"\n"
		slab_string = general_dos_string_generator(atom_ranges_slab_string)
		pDOS_string += slab_string
		return pDOS_string
	else:
		return pDOS_string

# algorithm for taking in comma and dash delimited
# range of atoms and expanding into the correctly
# formatted atom number list with coefficients for the
# pDOS calculation
def general_dos_string_generator(some_string):
	temp = some_string.split(',')
	expanded_list=[]
	for i in range(len(temp)):
		if "-" in temp[i]:
			ind = temp.index(temp[i])
			insert_list = temp[i].split('-')
			bi = int(insert_list[0])
			ei = int(insert_list[1])
			for j in range((ei-bi)+1):
				expanded_list.append(str(bi+j))
		elif not "-" in temp[i]:
			expanded_list.append(temp[i])
	temp = expanded_list
	temp_string = "atoms "
	for i in range(len(temp)):
		if ((i%10 == 0) and (i != 0)):
			temp_string += " \\\n{:s} 1,".format(temp[i])
		elif (i < (len(temp)-1)):
			temp_string += "{:s} 1, ".format(temp[i])
		elif (i == (len(temp)-1)):
			temp_string += "{:s} 1".format(temp[i])
	return temp_string
		

# generates generic name prefix from
# filename dilimeted by full stops '.'
def getfname():
	prefix=""
	for i in range(1,len(sys.argv)):
		if '.' in sys.argv[i]:
			if (prefix!=""):
				prefix=prefix+"-"+sys.argv[i].strip().split('.')[0]
			else:
				prefix=prefix+sys.argv[i].strip().split('.')[0]
	return prefix

# takes in a list of matrices to be
# merged into a single matrix for output
# the matrix is blocked such that mat[0]
# comes before mat[1] in out mat
def mergeMat(mat):
	dim=len(mat)
	temp=[]
	for i in range(dim):
		for j in range(len(mat[i])):
			temp.append(mat[i][j])
	mat=temp
	return temp

# reads custom_parameters.dat
def read_custom_parameters(custom_bool):
	if (custom_bool == True):
		if (os.path.exists('./custom_parameters.dat')):
			line_count = 0
			param_dict = {}
			key_sum = 0 # sanity check for debugging, should equal num atoms after file-parsing
			with open('./custom_parameters.dat','r') as fparams:
				curr_keys = []
				last_keys = []
				for line in fparams:
					line = line.strip()
					if ( not '#' in line ): # ignores comments :)
						line_count += 1
						if ( line_count == 1 ): # atom range lines
							last_keys = curr_keys
							curr_keys = expand_range_to_list(line)
							try:
								curr_keys = map(int,curr_keys)
							except ValueError:
								pass
						elif ( line_count == 2 ): # 
							curr_val = line
							line_count = 0
							if (( len(curr_keys) > 0 ) and ( curr_keys != last_keys )):
								for i in range(len(curr_keys)):
									if (not curr_keys[i] in param_dict.keys()):
										param_dict[curr_keys[i]] = curr_val
										key_sum+=1
									elif (curr_keys[i] in param_dict.keys()):
										if (param_dict[curr_keys[i]] != curr_val):
											sys.stderr.write("Cannot not designate two sets of parameters for same atom, exiting...\n")
											sys.exit()
										elif (param_dict[curr_keys[i]] == curr_val):
											sys.stderr.write("Detected two or more parameter sets for same atom, skipping the following set\n"+curr_val)
		return param_dict
	elif (custom_bool != True):
		param_dict = {} # return a blank dict cause we aint got no custom params today
		return param_dict

# takes a string of numbers separated by commas,
# and pairs of numbers separated by hyphens and
# expands to a complete list of all numbers
# covered by range specified in input string.
def expand_range_to_list(string_range):
	temp = string_range.split(',')
	expanded_list=[]
	for i in range(len(temp)):
		if "-" in temp[i]:
			ind = temp.index(temp[i])
			insert_list = temp[i].split('-')
			bi = int(insert_list[0])
			ei = int(insert_list[1])
			for j in range((ei-bi)+1):
				expanded_list.append(str(bi+j))
		elif not "-" in temp[i]:
			expanded_list.append(temp[i])
	return expanded_list

# handles situation where user provides two
# filename arguments, one for the adsorbate
# and one for the slab com file
if (len(sys.argv)==3):
	alabels=getatomlabels(sys.argv[1],ftype) # grab atom labels for printing later [adsorbate]
	blabels=getatomlabels(sys.argv[2],ftype) # grab atom labels for printing later [slab]

	# needed for dumping to bind only
	# helps that these are global
	natma=len(alabels) # num atoms [adsorbate]
	natmb=len(blabels) # num atoms [slab]
	if (natma != natms_ads):
		print "please check user-specification for natms_ads"
	if (natmb != natms_slab):
		print "please check user-specification for natms_slab"
	
	acoords=getcoords(sys.argv[1],ftype) # grab coordinates [adsorbat]
	acoords=convMatStr2MatFloat(acoords,2) # convert from string to float [adsorbate]
	bcoords=getcoords(sys.argv[2],ftype) # grab coordinates [slab]
	bcoords=convMatStr2MatFloat(bcoords,2) # convert from string to float [slab]

	tv=gettv(sys.argv[2]) # grab lattice vectors from comfile [slab]
	tv=convMatStr2MatFloat(tv,1) # convert a,b,c from string to float 

	tmat=maketmat(tv,1) # generate transformation matrix

	acoords=transform(acoords,tmat) # trasform to fractional coordinates [adsorbate]
	bcoords=transform(bcoords,tmat) # trasform to fractional coordinates [slab]

	labels=[blabels,alabels] # slab then adsorbate ordering
	coords=[bcoords,acoords] # slab then adsorbate ordering
	
	# merging labels and coords of daughter files for dumping to file
	labels=mergeMat(labels)
	coords=mergeMat(coords)

	dumpfraccoords(labels,coords,tv,outtype) # dump transformed coordinates

# handles situation where user provides one
# filename only. This script can't read your
# mind, so you should expect to manually modify
# the partitioning scheme in the ouput for what
# is defined as the donor/adsorbate becuase
# chances are what is done here is not what
# you wanted ^___^ (it is defined by construction
# for the two file branch logic above)
elif(len(sys.argv)==2):
	labels=getatomlabels(sys.argv[1],ftype) # grab atom labels for printing later [adsorbate]

	natma=natms_ads # number of adsorbate atoms
	natmb=natms_slab # number of slab atoms
	
	coords=getcoords(sys.argv[1],ftype) # grab coordinates [adsorbat]
	coords=convMatStr2MatFloat(coords,2) # convert from string to float [adsorbate]

	tv=gettv(sys.argv[1]) # grab lattice vectors from comfile [slab]
	tv=convMatStr2MatFloat(tv,1) # convert a,b,c from string to float 

	tmat=maketmat(tv,1) # generate transformation matrix

	coords=transform(coords,tmat) # trasform to fractional coordinates [adsorbate]

	basis_num_list = gen_basis_num_list(labels,basis,absorbing_atoms)

	param_dict = read_custom_parameters(custom_params) # get custom parameters from custom_parameters.dat

	dumpfraccoords(labels,coords,tv,outtype,basis_num_list,param_dict) # dump transformed coordinates

	



