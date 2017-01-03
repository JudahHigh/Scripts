Title: analyzeTDDFT.py
Author: Judah High
Status: Functional

Description: parses the output of a Gaussian TD-DFT calculation located in the
log file (.log ext) and generates a text file that may be loaded into excel
using the ';' character as a dilimeter to create tables for inspecting analyzing
the character of the calculated excited states easier than by examining the
raw data located in the log file.

Use: User passes the (1) log file as arg-1 and (2) a prefix for the text file
as arg-2,

>> python analyzeTDDFT.py znp.log znp

generates znp-excitations.txt. This file may be opened in Microsoft Excel using
the ';' character as a dilimeter.
