Title: work_on_all_curr_dir_files.py
Author: Judah High
Status: Functional

Description: Runs a python script on all files in the current working directory
with a specified file-extension. If the python script to run takes arguments,
the first argument MUST be a file with the specified file-extension.

Use: Within a directory with files to be worked on, the user passes the (1)
file-extension, (2) python script to be used that is also in the current
working directory and (3) any other arguments needed for the second python
script to run excluding the first mandatory filename argument.

>> python work_on_all_curr_dir_files.py com conv_to_xyz.py

The example above which may be run in the test directory included will convert
each .com file in the test directory to an .xyz via the conv_to_xyz.py script
and subsequently store these generated .xyz flies in another sub-directory
called new_wdir.
