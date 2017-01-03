import os
import sys
import re

# User specification of a,b,c translation vectors to
# be added at the end of the coordinates within a
# an com file passed as argument
tvline="Tv\t30.49498400\t0.00000000\t0.00000000\n"
tvline=tvline+"Tv\t0.00000000\t31.46113821\t0.00000000\n"
tvline=tvline+"Tv\t0.00000000\t0.00000000\t45.00000000\n"

# filename argument... MUST BE COM FILE or WILL NOT work
filename=sys.argv[1]

# get the file prefix before .com extension
# used to generate unique output filename
prefix=filename.strip().split('.com')[0]
suffix='_addtv.com'
ifname=prefix+suffix

# begin algorithm to insert com files
blank_count=0 # number of blank lines encountered in com file (is a signal)
ofstream=open(ifname,'w') # open output file stream
with open(filename,'r') as input_file: # parse input file stream
	for line in input_file: # get each line from istream
		# if blank line then increase number of blank lines found
		if ( line == '\n' ):
			blank_count+=1
		# after the coordinate section write the new Tv lines
		if (blank_count==3):
			ofstream.write(tvline)
			blank_count=100
		# writes every line from input file EXcluding any existing Tv lines
		if (blank_count!=3):
			if (not "Tv" in line):
				ofstream.write(line.strip()+'\n')
		
