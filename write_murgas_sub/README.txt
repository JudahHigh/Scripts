Title: write_sub.py
Author: Judah High
Status: Functional

Description: Given an input file, will create a submission script for a
calculation on a cluster that will use the input file given. Currently
the user must hard-code the lines necessary to create a correct submission
script in write_sub.py.

The advantage to using this script is that if one submits a lot of calculations
on cluster with similar resource requirements and that use the same program,
then instead of manually creating potentially hundreds or thousands of
independent submission scripts, the user can simply run this script on all input
files to create each individual submission script in one stroke.

Eventually this script will be generalized to not only recognize file-
extensions and the associated programs that take these files as arguments,
but to also use the current environment to recognize which cluster is being
used and if it is a new cluster, resort to user-defined lines to format the
submission script. Full automation of this process is the end-game however
it is second-priority to my current research and will not make a large enough
impact short-term, but the long-term payoffs in conjunction with other scripts
I have written have a huge impact on streamlining very time-consuming perpatory
and analysis steps in the computational research process... especially on
projects where a student may juggle thousands of files on a regular basis.

Use: User simply provides the input file as an argument to the script. Don't
forget to hardcode the lines for the submission script into write_sub.py before
use.

>> python write_sub.py some_molecule.com


