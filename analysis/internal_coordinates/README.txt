Title: int_coord_analysis.py
Author: Judah High
Status: Near completion

Description: This script takes as an argument a molecular input file and will
return a formatted list of all of the unique internal coordinates of the
molecule, that is bond lengths, bond angles and dihedral angles. These are the
internal coordinates by which the normal modes of vibration of a molecule are
determined.

The ultimate use off this script is to track these internal coordinates during
molecular dynamics simulations to compute statistics on the average dynamics of a 
system in time.

So far the script is capable of generating all bond lengths and bond angles and
the algorithm for extracting all unique dihedral angles is nearly complete.

This script is being programmed to be general for type of atom connectivity or
node topology ( each node is an atom ). For example, the script can handle both
linear, cyclic and 3D structures.

Use: The user passes a Gaussian input file (.com extension) with connectivity
information to the script.

>> python int_coord_analysis.py some_molecule.com

The working version will convey a list of all internal coordinates to the user
in some way. 
