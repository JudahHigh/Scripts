Title: transSys.py
Author: Judah High
Status: functional

Description: Moves the coordinates of atoms within the specified Gaussian
input file (.com extension) by an amount specified by the user in either
the local x, y or z direction.

Use: User specifies three arguments (1) the input .com file conaining the
coordinates, (2) the direction of translation and (3) the amount of translation
in Angstroms.

>> python transSys.py some_molecule.com x 1.0

generates an output file with the "-trans.com" suffix to the prefix of the
input file name without its file-extension (some_molecule) in the example case.
