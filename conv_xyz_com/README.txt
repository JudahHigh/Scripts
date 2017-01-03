Title: conv_to_xyz.py
Author: Judah High
Status: Complete

Description: This a simply yet very powerful script for the convenience it gives
the user in allowing one to easily convert between the .xyz and .com file formats.
This was sorely needed for my research do to a number of steps I needed to take
on a regular basis converting files between these two molecular file formats...
manually.

If passed a .com file, the script generates a .xyz file from the coordinates.
If passed a .xyz file, the script generates a .com file from the coordinates.

Use: Pass the script either a .com or .xyz molecular input file,

>> python conv_to_xyz.py some_molecule.com

and the a file will be created using the other file format, some_molecule.xyz
in the example.

