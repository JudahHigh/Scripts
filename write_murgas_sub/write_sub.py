import os
import sys
import subprocess

# writes a custom submission script
# after encountering a known input file
# 
# this script will eventually recognize known
# file types and create corresponding submit
# scripts
#
# right now the user must specify the lines
# necessary to write the submit script correctly
# including the use of the input file usually
# as an argument passed to a program for use on
# the cluster.

def main():
	curr_dir = os.getcwd()

	flist = os.listdir(curr_dir)

	input_file = ""
	for i in range(len(flist)):
		curr_file_path = curr_dir+"/"+flist[i]
		if (os.path.isfile(curr_file_path)):
			if (".bind" in flist[i]):
				input_file = "./"+flist[i]
				break

	command = "./dynamics "+input_file

# USER SHOULD SPECIFY THE LINES NECESSARY FOR THE CLUSTER
# SPECEFIC SUBMISSION SCRIPT HERE. Below are lines for a
# cluster that I have heavily used.
	submit_script="#!/bin/sh\n\
#These commands set up the Grid Environment for your job:\n\
#PBS -N "+curr_dir+"\n\
#PBS -jeo\n\
##PBS -e error\n\
##PBS -o output\n\
#PBS -l pmem=2GB,nodes=1:ppn=1,walltime=302:00:00\n\
#########\n\n\
# runs job from the current working directory\n\
RUNDIR=$PBS_O_WORKDIR\n\
export RUNDIR\n\
cd $RUNDIR\n\n\
#print the time and date\n\
date\n\n\
"+command+"\n\n\
#print the time and date again\n\
date\n"

	sys.stdout.write("    will now create \"sub\" file in "+curr_dir+"\n")

	sys.stdout.write("      opening \"sub\" file\n")
	sub_file = open("sub",'w')
	sys.stdout.write("      writing \"sub\" file\n")
	sub_file.write(submit_script)
	sys.stdout.write("      closing \"sub\" file\n")
	sub_file.close()

	sys.stdout.write("    adding executable permissions to \"sub\" file\n")
	subprocess.call(['chmod +x sub'],shell=True)

if __name__ == "__main__":
	main()


