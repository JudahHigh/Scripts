Title: do_cmd_in_all_sub_dirs.py
Author: Judah High
Status: Functions/known bugs

Description: Performs a given command within any sub-directory of the current
working directory. For example one could run a python script of some kind
inside each sub-directory.

Use: Pass command as argument to script. Current version cannot accept special
tokens like '|,<<,>>,<,>'

>> python do_cmd_in_all_sub_dirs.py python write_murgas_sub.py

The above example runs a script that looks for a .com file in each sub-directory
and creates a submit script for a cluster running Gaussian with that .com input
file.

