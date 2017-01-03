#!/bin/bash
import os
import sys
import re
import shutil

# file to be converted
infile=sys.argv[1]

# filetype... either xyz or com
ftype=infile.strip().split('.')[len(infile.strip().split('.'))-1]

xyz_to_com=False
com_to_xyz=False

if (ftype=="xyz"):
	xyz_to_com=True
if (ftype=="com"):
	com_to_xyz=True

if xyz_to_com:
	# read atom ids and coords
	coords=[]
	ids=[]
	linecount=0
	with open(infile,'r') as isfile:
		for line in isfile:
			linecount+=1
			if ( linecount > 2 ):
				line=line.strip().split()
				ids.append(line[0])
				for i in range(1,4):
					coords.append(line[i])
	isfile.close()

	# make list of unique atom ids
	uids=[]
	for i in range(len(ids)):
		if ( not ids[i] in uids ):
			uids.append(ids[i])

	# create new file name based on input file name
	ofprefix=infile.strip().split('.xyz')[0]
	ofsuffix=".com"
	ofname=ofprefix+ofsuffix

	# make sure output .com file doesn't exists
	if ( os.path.exists("./"+ofname) ):
		print "the .com file to be generated called "+ofname+" already exists... exiting"
		sys.exit()

	# print atom ids and coords in com format
	outfile=open(ofname,'w')
	outfile.write("%chk="+ofprefix+".chk\n%mem=24GB\n%nproc=12\n#p b3lyp/6-31G*\n\ntitle\n\n0 1\n")
	for i in range(len(ids)):
		outfile.write(ids[i]+"\t")
		outfile.write(coords[i*3]+"\t"+coords[i*3+1]+"\t"+coords[i*3+2]+"\n")
	outfile.write("\n")
	for i in range(len(uids)):
		outfile.write(uids[i]+" ")
	outfile.write("0\n6-31G*\n****\n\n")
	outfile.close()

if com_to_xyz:
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

	# create new file name based on input file name
	ofprefix=infile.strip().split('.com')[0]
	ofsuffix=".xyz"
	ofname=ofprefix+ofsuffix

	# make sure output .com file doesn't exists
	if ( os.path.exists("./"+ofname) ):
		print "the .xyz file to be generated called "+ofname+" already exists... exiting"
		sys.exit()

	# print atom ids and coords in xyz format	
	outfile=open(ofname,'w')
	outfile.write(str(natoms)+"\n")
	outfile.write("title\n")
	for i in range(len(ids)):
		outfile.write(ids[i]+"\t")
		outfile.write(coords[i*3]+"\t"+coords[i*3+1]+"\t"+coords[i*3+2]+"\n")
	outfile.close()
		
	

