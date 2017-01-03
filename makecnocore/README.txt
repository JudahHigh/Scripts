Title: makecnocore.py
Author: Judah High
Status: Functional

Description: At one point during my research it was necessary to find a way to
project DFT level molecular orbitals onto the EH level of theory. What this is
essentially asking for is a projection of a set of orthonormal one-electron
wavefunctions onto a lower-dimension basis set used to expand these
wavefunctions as a linear combination of atom orbital basis functions. This is
a difficult task to perform.

The steps for my research involved projecting from a 6-31G* basis to an STO-6G
basis and than to a STO basis with no basis functions corresponding to "core"
atomic orbitals like the 1s-orbital of a carbon atom for example.

Furthermore in my research a different program called DynEMol was used for the
extended Huckel calculations while the initial projection (6-31G* --> STO-6G)
was done with Gaussian. Unfortunately the inherent ordering of basis functions
in Gaussian is different than DynEMol and thus the final step, that this script
handles, is a (1) projection from STO-6G to STO basis with no core orbitals and
rearrangement of the resulting projected MO coefficients to be read in by
DynEMol with its inherent basis function ordering.

The script produces a simple output file with three columns (1) basis function
number at projected basis, (2) basis function number and (3) new coefficient.

Use: The user must at least pass in a number for the STO-6G MO to be projected
followed by a '-' char followed by the corresponding EH MO number. For example
the highest occupied molecular orbital (HOMO) of a molecule abbrieviated FbP is
MO 208 at the STO-6G level with core and valence electrons. At the EH level
with no core electrons the HOMO is MO 148... without core orbitals and
electrons, the total number of electrons goes down and thus the HOMO is a lower
number MO. For this example with FbP to produce the projected coefficients the
user would issue the following  command,

>> python FbP.fchk 208-148

This would generate "cnocore.dat" which contains the projected coefficients.

I developed a subroutine which I incorporated into DynEMol to read in and use
these projected coefficients during a genetic algorithm done at the extended
Huckel level, which I developed.
