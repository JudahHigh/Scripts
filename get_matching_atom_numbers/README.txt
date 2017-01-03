Title: get_matching_atom_numbers.py
Author: Judah High

Description: User passes in two Gaussian input files (.com extensions), call
them a.com and b.com. If atoms in b.com exist in a.com, an atom range string
is printed to standard output showing the atom-numbers in b.com that are in
a.com

Use: Pass two .com input files to script. Atom numbers of the second file that
are in the first will be printed to standard output.

This script is critical for getting some of the user-defined parameters
necessary to make IETsim .bind input files using bindMaker.py, another
script I have programmed.

>> python get_matching_atom_numbers.py a.com b_in_a.com

The output of this might be the string "1-288" meaning that atoms 1 through
288 in b_in_a.com exist in a.com as well.
