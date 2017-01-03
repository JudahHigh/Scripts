Title: num_huckel_electrons.py
Author: Judah High

Description: This script takes in a molecular input file for Gaussian and
prints out the number of electrons that the extended Huckel (EH) Hamiltonian
would use to describe the molecule. EH only considers valence electrons.
Carbon, for example has 6 electrons, but EH only sees 4, the 2-2s electrons
and the 2-2p subshell electrons. Of course in reality these electrons are
not confined to orbitals, but as a chemist I use MO theory for accounting
reasons and EH theory is based on MO theory so it neglects core electrons
distinguishing them from valence electrons in that their not involved in
chemistry (I know, violation of indistinguishability of quantum particles).

When dealing with large systems determining the number of EH electrons can
be quite tricky, so this script does the heavy lifting for the user.

Use: The user passes a Guassian input file (.com extension) to the script as
an argument.

>> python num_huckel_electrons.py some_molecule.com

The number of EH electrons for the input file is printed to standard output.
