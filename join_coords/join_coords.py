import os
import sys
import re
from copy import deepcopy

def read_com(infile):
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

	return ids,coords,natoms

def join_coords(ids_a,coords_a,natoms_a,ids_b,coords_b,natoms_b):
	ids=deepcopy(ids_a)
	coords=deepcopy(coords_a)
	natoms=natoms_a+natoms_b
	for i in range(len(ids_b)):
		ids.append(ids_b[i])
		for j in range(3):
			coords.append(coords_b[(i*3)+j])
	return ids,coords,natoms

def print_joined_coords(ids,coords,natoms,infile_a,infile_b):
	# make list of unique atom ids
	uids=[]
	for i in range(len(ids)):
		if ( not ids[i] in uids ):
			uids.append(ids[i])

	# create new file name based on input file name
	ofprefix_a=infile_a.strip().split('.com')[0]
	ofprefix_b=infile_b.strip().split('.com')[0]
	ofsuffix=".com"
	ofname="joined_"+ofprefix_a+"_"+ofprefix_b+ofsuffix

	# make sure output .com file doesn't exists
	if ( os.path.exists("./"+ofname) ):
		print "the .com file to be generated called "+ofname+" already exists... exiting"
		sys.exit()

	# print atom ids and coords in com format
	outfile=open(ofname,'w')
	outfile.write("%chk=joined.chk\n%mem=24GB\n%nproc=12\n#p b3lyp/6-31G*\n\njoined_"+ofprefix_a+ofprefix_b+ofsuffix+"\n\n0 1\n")
	for i in range(len(ids)):
		outfile.write(ids[i]+"\t")
		outfile.write(coords[i*3]+"\t"+coords[i*3+1]+"\t"+coords[i*3+2]+"\n")
	outfile.write("\n")
	for i in range(len(uids)):
		outfile.write(uids[i]+" ")
	outfile.write("0\n6-31G*\n****\n\n")
	outfile.close()

# read two molecular input files to join
infile_a = sys.argv[1]
infile_b = sys.argv[2]
if (infile_a==infile_b):
	print "Won't merge "+infile_a+" "+infile_b+"... same file"
	sys.exit()

# fill atom arrays with atom ids and coordinates
# gathered from input file arguments
ids_a,coords_a,natoms_a = read_com(infile_a)
ids_b,coords_b,natoms_b = read_com(infile_b)

# merge the atom information arrays together
ids,coords,natoms = join_coords(ids_a,coords_a,natoms_a,ids_b,coords_b,natoms_b)

# output joined atom coordinates to new input file
# using naming convention "joined_[filename_a]_[filename_b].com
print_joined_coords(ids,coords,natoms,infile_a,infile_b)



