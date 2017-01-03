Title: moVecAngle.f90
Author: Judah High
Status: Functional

Description: Takes two formatted checkpoint files for two Gaussian calculations
where the number of basis functions and atoms are identical for each. The files
(.fchk extension) are parsed and the MO coefficients in each are extracted and
stored. These coefficients are normalized such that the sum of the square of 
each MOs coefficients are unity. After which the projection of each MO from
one file is taken on each MO of the other file. The resulting MO angles are
stored in a file called "angles.dat" Should the user wish to filter the
angles that are stored, If statements may be added to the last block of
code before the end of the program block.

The MO angles were useful for the evaluation of MO quality generated from
approximate quantum mechanical procedures which approximate the time-
independent wavefunction to be single-determinantal in nature.

Use: Upon compilation pass the two formatted checkpoint files as arguments
to the executable.

>> ./a a.fchk b.fchk

