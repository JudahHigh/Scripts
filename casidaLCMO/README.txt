Title: casidaLCMO.py
Author: Judah High
Status: Functional

Description: User passes a (1) TD-DFT log file generated by Gaussian (.log ext)
and (2) an excited state of choice (1, 2, ... , n) and the script will
calculate coefficients to form an electron and hole LCMO that together
model the change in the ground-state density upon vertical excitation to
the specified excited state. The procedure to obtain the coefficients from
the transition densities of a given excitation given in the .log file was
developed by me and can be found in J. Phys. Chem. A. 2016, 120(41), 8075-8074.

Use: pass log file as arg-1 and choice of excited state as arg-2

>> python casidaLCMO.py some_molecule.log 1

will generate output similar to the following,

ELECTRON LCMO ::    209   0.7141737480250215   210   0.6999684690269221
HOLE     LCMO ::    208   0.8068521000614925   207   0.5907534922675949
