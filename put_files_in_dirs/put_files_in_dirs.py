import os
import sys
import shutil
import argparse
import subprocess
import stat

# takes a source directory as the argument, NOT THE PATH
# JUST THE SRC DIR NAME

# puts files within the source dirs name into all sub-directories
# within the current working directory file structure

def check_args(args):
	if len(args) == 2:
		return True
	else:
		return False

def put_files_in_dirs(args):
	srcdir = args[1]
	sys.stdout.write("Source directory: "+srcdir+"\n")

	currdir = os.getcwd()
	dirlist = os.listdir(currdir)

	srcdirlist = os.listdir(currdir+"/"+srcdir)

	uid = os.getuid()
	gid = os.getgid()

	for i in range(len(dirlist)):
		put_dir = dirlist[i]
		if (os.path.isdir(currdir+"/"+put_dir)):
			if ( put_dir != srcdir ):
				sys.stdout.write("Copying files from "+srcdir+" to "+put_dir+"\n")
				for j in range(len(srcdirlist)):
					src_path = currdir+"/"+srcdir+"/"+srcdirlist[j]
					dest_path = currdir+"/"+put_dir+"/"+srcdirlist[j]
					try:
						shutil.copyfile(src_path,dest_path)
						if (stat.S_IXUSR & os.stat(src_path)[stat.ST_MODE]):
							sys.stdout.write("  "+srcdirlist[j]+" file is executable... changing destination file permission accordingly\n")
							subprocess.call(['chmod +x '+dest_path],shell=True)
						else:
							sys.stdout.write("  "+srcdirlist[j]+" file not executable\n")
					except shutil.Error:
						sys.stderr.write("shutil.copy error ?\n")

def main(args):
	if (check_args(args)):
		put_files_in_dirs(args)
	else:
		sys.stderr.write("needs an argument\n")
		sys.exit()

if __name__ == "__main__":
	main(sys.argv)
