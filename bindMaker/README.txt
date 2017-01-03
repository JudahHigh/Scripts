Title: bindMaker.py
Author: Judah High
Status: Complete

Description: This script creates input files for a quantum dynamics program
called IETsim developed by Luis G.C. Rego and Victor Batista on top of an EH
program called yaehmop developed largely in part by Greg Landrum at Cornell.

The input files (.bind extension) contain many sections including, but not
limited to,

 - Crystollographic information
 - Custom EH parameters
 - Partial density of states specification
 - Survival probability specification
 - Quantum dynamics parameters
 - Cube file generation flags
 - Absorbing potential specification

Each of the above sections are quite difficult to prepare manually and very
error-prone. Fortunately the IETsim package has a limited input file generator,
however the included script is simply not capable of handling the input file
generation demands of this group where thousands of these input files need to
be generated and all done with 100% correctness. The stock script is incapable
of initializing many of the sections shown above.

The script I have written here
was written from scratch to overcome the massive shortcomings of the stock bind
making script that comes with IETsim. It was also developed in conjunction with
a few other powerful scripts that will help the user set up what's necessary for
this script.

To use, the user simply defines the parameters in the user-defined parameter
section of the script in regards to molecular specifications, the script will
handle the rest.

Use: pass an .xyz molecular input file to the script. If a "custom_parameters.dat"
file is present in the current working director, custom EH parameters will be read
and used when preparing the .bind input file.

>> python bindMaker.py some_molecule.xyz

