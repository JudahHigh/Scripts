Title: moegetter.py
Author: Judah High

Description: moegetter stands for MO energy getter. The user gives the script
a DynEMol or IETsim MO energy output file, system-ergs.dat or [prefix].bind.out
along with a specification of either eV or au as the output MO energy unit.

The script prints the MO energies with the specified unit of choice and creates
a Guassian like formatted checkpoint file with the given energies for use by 
another script used for plotting purposes.

Use: pass the MO energy file along with specification of either eV or au units

>> python moegetter.py system-ergs.dat ev

or

>> python moegetter.py example.bind.out au
