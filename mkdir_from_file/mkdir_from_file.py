import os
import sys
import os
import shutil

# takes any file as input dilemited by full-stops
# makes directory based on filename and puts input
# file inside of it

filename = sys.argv[1]
dirname = sys.argv[1].strip().split('.')[0]
currentdir = os.getcwd()
newdirpath = currentdir+"/"+dirname

frompath = currentdir+"/"+filename
topath = newdirpath+"/"+filename

if (not os.path.exists(newdirpath)):
	os.mkdir(newdirpath)
	shutil.move(frompath,topath)
else:
	sys.stderr.write("error: \""+dirname+"\" dir already exists\n")
