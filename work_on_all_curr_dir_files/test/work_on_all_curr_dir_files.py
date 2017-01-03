import os
import sys
import subprocess
import shutil
#import conv_xyz_com

# finds all files in current directory with
# file extension given by first argument

# runs python script on all files in current
# directory with specified file-extension.
# python script name passed as second argument

extension=sys.argv[1]

python_script=sys.argv[2]

script_args=''
#script_args=script_args.join(map(str,(sys.argv[3:len(sys.argv)])))
for arg in sys.argv[3:len(sys.argv)]:
	script_args=script_args+arg+" "
script_args=script_args.strip()

# get a listing of all files in cwd
filenames = next(os.walk(os.getcwd()))[2]

# filter out all files except those with a given extension
work_files=[]
for i in range(len(filenames)):
	if ( filenames[i].strip().split('.')[len(filenames[i].strip().split('.'))-1] == extension ):
		work_files.append(filenames[i])

# for every file with extension, do xyz -> com or com -> xyz
for i in range(len(work_files)):
#	conv_xyz_com.main(work_files[i])
	subprocess.call(['python '+python_script+' '+script_args+' '+work_files[i]],shell=True)

# transfer all files to a new working directory
try:
	os.mkdir("./new_wdir")
except OSError:
   print "./new_wdir directory already exists"
   print "in "+os.getcwd()+"\n"
new_filenames = next(os.walk(os.getcwd()))[2]
for filename in new_filenames:
	if ( not filename in filenames):
		try:
			if os.path.exists("./"+filename):
				shutil.move("./"+filename,"./new_wdir/")
			else:
				pass
		except shutil.Error, e:
			print "\nfile "+filename+" already created in new_wdir... skipping move\n"
			os.remove("./"+filename)


