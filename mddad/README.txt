Title: mddad.py
Author: Judah High
Status: Functional

Description: Parses through a input trajectory file with .xyz formatting from
a molecular dynamics simulations and records the value of a specified
internal coordinate into "internal_coords.dat" for each of the n-steps
specified by the user.

Use: User passes (1) .xyz trajectory file (2) number of steps to parse and
1 to four atom numbers to specify an internal coordinate to measure in
each frame.

>> python mddad test.out.xyz 8 1 2 3 4
