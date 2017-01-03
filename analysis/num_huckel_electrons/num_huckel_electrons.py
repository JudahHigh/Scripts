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

# Gets the number of huckel electrons for a
# given atom from a pre-made dictionary of
# atom labels as keys and number of electrons 
# as values.
def getNumHuckelElectronsForAtom(atom_id):
	id_nelec_dict = { "H" : 1, "C" : 4, "N" : 5, "Zn" : 2, "O" : 6, "B" : 3, "F" : 7 }
	if ( atom_id in id_nelec_dict.keys() ):
		return id_nelec_dict[atom_id]

# Gets the total number of Huckel electrons for
# entire molecule
def getNumHuckelElectronsForMolecule(atom_ids):
	n_elec=0
	for i in range(len(atom_ids)):
		n_elec += getNumHuckelElectronsForAtom(atom_ids[i])
	return n_elec


ids,coords,natoms = getMolecule(sys.argv[1])
nelec = getNumHuckelElectronsForMolecule(ids)
print nelec
























