import os
import sys
import re
import shutil

def getFileExtension(filename):
	fext = filename.strip().split('.')[len(filename.strip().split('.'))-1]
	return fext

def readCom(infile):
	# initalize atom coords and id arrays
	ids=[]
	coords=[]

	# read atom ids and coords
	blank_line_count=0
	coord_line_count=0
	with open(infile,'r') as isfile:
		for line in isfile:
			if ( blank_line_count == 2 ):
				if ( coord_line_count == 0 ): # upon entering should set coord_line_count to 1
					coord_line_count+=1
					continue
				if ( coord_line_count > 0 ) and ( line != "\n" ): # first time to enter coord_line_count should equal 1
					if ( not "Tv" in line ):
						line=line.strip().split()
						ids.append(line[0])
						if ( len(line) == 4 ): # no special flags between atom id and coordinates
							for i in range(1,4):
								coords.append(line[i])
						elif ( len(line) > 4 ): # if special flags present between atom id and coordinates
							for i in reversed(range(len(line)-3,len(line))):
								coords.append(line[i])
						else:
							print "Not all x, y and z coordinates present on one or more lines in .com file..."
							sys.exit()
						coord_line_count+=1
			if ( line == "\n" ):
				blank_line_count+=1
			if ( blank_line_count == 3):
				break

	# compute the number of atoms
	natoms=len(ids)
	if ( len(ids) != len(coords)/3 ) or ( len(coords)/3 != len(ids) ):
		print "number of atoms and coords in .com file do not match up"
	
	return ids, coords, natoms

# function obtains the molecules coordinates and
# atom labels in separate arrays. The number of
# atoms is then computed and used in a sanity check.
# Function takes a filename as argument.
def getMolecule(infile):
	if ( getFileExtension(infile) == "com" ):
		ids,coords,natoms = readCom(infile)
		return ids, coords, natoms

# determines the number of atoms of types
# within molecule, like the number of carbon
# atoms for example
def getNumTypesOfAtoms(ids):
	num_types={}
	for i in range(len(ids)):
		if ( not ids[i] in num_types.keys() ):
			num_types[ids[i]] = 1
		if ( ids[i] in num_types.keys() ):
			num_types[ids[i]] += 1
		else:
			pass
	return num_types

def printTypes(num_types):
	for k,v in num_types.items():
		sys.stdout.write("Atom Type: {:s}, Number: {:d}\n".format(k,v))


ids,coords,natoms = getMolecule(sys.argv[1])
num_types = getNumTypesOfAtoms(ids)
printTypes(num_types)
























