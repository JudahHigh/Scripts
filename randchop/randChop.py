#!/usr/bin/python

from random import randint
import os
import sys
import subprocess
import shutil

print "BEGIN CHOPPING ALGORITHM\n"

xyzfile=sys.argv[1]
nchops=int(sys.argv[2])
choparray=[]
chopoffset=10
chopmax=30

# use subprocess to determine number of lines in .xyz file
cmd='wc -l '+sys.argv[1]
p=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=p.communicate()
nlines=int(out.split()[0])

# use subprocess to find number of atoms (first line of file)
cmd='head -1 '+sys.argv[1]
p=subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=p.communicate()
natms=int(out)

# compute number of frames
# header is 2 lines
# body is natms-lines long
nframes=(nlines / (natms+2))+1

# print data algorithm determined
# frm the xyz file provided
print "number of lines in xyz    ::\t"+str(nlines)
print "number of atoms from xyz  ::\t"+str(natms)
print "number of frames from xyz ::\t"+str(nframes)+"\n"

# generate random sequence of chops
# between the end of the equilibration
# period (chopoffest) and last frame (chopmax)
if ((chopmax-chopoffset+1) < nchops):
	print "choprange can't be less than the number of chops..."
	print "exiting"
	sys.exit()
while (len(choparray) != nchops):
	frame=randint(chopoffset,chopmax-1)
	if ( not frame in choparray):
		choparray.append(frame)

# format print of the chops selected at random
print "Randomly Selected Frames to Chop"
tempstring=""
for i in range(len(choparray)):
	if ( i%10 == 0 ):
		print tempstring
		tempstring=""
	else:
		tempstring+=str(choparray[i])+" "
print ""

# make frame directory
try:
	os.mkdir("chopped_frames")
except OSError:
	print "chopped_frames dir already exists"
	print "in "+os.getcwd()+"\n"

# open xyz and chop out frames once parsed
prefix="00000000"
fcount=0
cpcount=0
ofopen=False
print "Chopping out selected frames from .xyz file\n"
with open(sys.argv[1]) as fp:
	for line in fp:
		if ( ("MD" in line) and ("iter" in line)):
#			fframe = line.strip().split()[len(line.strip().split())-1] # uncomment if frames are ordered 0 - nframes in .xyz file
			fframe=str(fcount) # comment if framese are ordered 0 - nframes in .xyz file
			if (int(fframe) in choparray):
				cp_frame_str=fframe
				ofname="f"+prefix[0:len(prefix)-len(fframe)]+fframe+".xyz"
				ofstream=open(ofname,'w')
				ofopen=True
				ofstream.write(str(natms)+"\n")
			fcount+=1
		if (ofopen):
			ofstream.write(line.strip()+"\n")
			cpcount+=1
		if cpcount==natms+1:
			print "chopped out frame "+cp_frame_str+" to "+ofname
			ofstream.close()
			try:
				shutil.move("./"+ofname,"./chopped_frames/")
			except shutil.Error, e:
				print "\nfile "+ofname+" already created in chopped_frames... skipping move\n"
				os.remove("./"+ofname)
			cpcount=0
			ofopen=False

print "\nEND CHOPPING ALGORITHM"
		
			
		

