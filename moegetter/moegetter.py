#!/usr/bin/python
import os
import sys
import re
from time import time

# Author: Judah High
# Organization: Dept of Chem, NCSU

# script will extract the MO energies from an IETsim ".out" file or a 
# DynEMol "system-ergs.dat" file.

# arg1 :: system-ergs.dat filename
# arg2 :: convert to eV or H, type 'eV' or 'H'

# this is a function that converts a sting to an integer or float if int
# doesn't work.
def convertStr(s):
	try:
		ret = int(s)
	except ValueError:
		ret = float(s)
	return ret

# returns True for ietsim and False
# for dynemol
def ietsim_or_dynemol(filename):
	if ( re.match(r'.*bind.out',filename) ):
		return "ietsim"
	elif ( re.match(r'system-ergs.dat',filename) ):
		return "dynemol"
	else:
		sys.stdout.write("Use a IETsim .bind.out file or a DynEMol system-ergs.dat file... exec term...\n")
		sys.exit()

# used to set a multiplicative constant to be used in converting the MO
# energies to the proper output units
def use_ev_or_au(units_flag):
	if ( re.match(r'[eE]{1}[vV]{1}|[eE]{1}lectron[-_]{1}[vV]{1}olts',units_flag)  ): # for eV --> eV conversion, I know... redundant, but necessary :)
		constant = 1.0
	elif ( re.match(r'[aA]{1}[uU]{1}|[hH]{1}artree',units_flag) ): # for eV --> au conversion
		constant = float(1.0/27.211396132)
	else:
 		constant = 1.0
	return constant

# read MO energies from file into list called
# ergs
def read_ergs(filename,program):
	with open(filename,'r') as fo:
		if ( program == "ietsim" ):
			ergs = [float(line.strip().split(':--->')[1]) for line in fo if ':--->' in line]
			return ergs
#			print "ietsim ergs",ergs,len(ergs)
		elif ( program == "dynemol"):
			ergs = [float(line.strip().split()[1]) for line in fo]
#			print "dynemol ergs:",ergs,len(ergs)
			return ergs
		else:
			sys.stdout.write("Unforseen error when reading file... exec term\n")

# extremely compact expression to print all MO energies
# to standard output :)
def print_energies(ergs,constant):
	map(lambda erg: sys.stdout.write('MO '+str(ergs.index(erg)+1)+' :: '+'{: 13.8f}\n'.format(erg*constant)),ergs)

# create fchk file with MO energies for use with get_mo_bar.sh
# to make a plotting file for the MO energies
def write_to_fchk(ergs,filename):
	conv_factor = 27.211396132
	with open(filename+'.fchk','w') as ofchk:
		ofchk.write('Alpha Orbital Energies                        R   N= {: 9d}\n'.format(len(ergs)))
		meat = '\n'.join([' {: 13.8E} {: 13.8E} {: 13.8E} {: 13.8E} {: 13.8E}'.format(ergs[i*5]/conv_factor,ergs[i*5+1]/conv_factor,ergs[i*5+2]/conv_factor,ergs[i*5+3]/conv_factor,ergs[i*5+4]/conv_factor) for i in range((len(ergs))/5)])
		cherry = ''.join([' {: 13.8E}'.format(ergs[(len(ergs)-((len(ergs))%5))+i]) for i in range(len(ergs)%5)])

		ofchk.write(meat+'\n'+cherry)
		ofchk.write('\nAlpha MO coefficients                         R   N= {: 9d}\n\n'.format((len(ergs)**2)))

def main(filename,units_flag):
	program = ietsim_or_dynemol(filename)
	constant = use_ev_or_au(units_flag)
	ergs = read_ergs(filename,program)
	print_energies(ergs,constant)
	write_to_fchk(ergs,filename)

if __name__ == "__main__":
	t1=time()
	main(sys.argv[1],sys.argv[2])
	t2=time()
	sys.stdout.write("time: {:8.4f} seconds\n".format(t2-t1))

