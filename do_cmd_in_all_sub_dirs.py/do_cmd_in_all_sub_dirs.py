import os
import sys
import subprocess

def check_args(args):
	if (len(args) > 2 ):
		return True
	else:
		sys.stderr.write("need at least two arguments [command] [file]\n")
		return False

def get_command(args):
	command=""
	for i in range(len(args)):
		if (( i < len(args)-1 ) and ( i > 0 )):
			command+=args[i]+" "
	return command

def get_command_argument(args,command):
	carg = args[len(args)-1]
	if (not carg in command):
		return carg
	else:
		return ""

def main(args):

	command = get_command(args)
	carg = get_command_argument(args,command)
	spcommand = command+carg
	sys.stdout.write("Command: "+spcommand+"\n")

	curr_dir = os.getcwd()
	root_path = curr_dir

	dir_list = os.listdir(curr_dir)


	for i in range(len(dir_list)):
		curr_element_path = curr_dir+"/"+dir_list[i]
		if (os.path.isdir(curr_element_path)):

			sys.stdout.write("entering directory "+curr_element_path+"\n")
			try:
				os.chdir(curr_element_path)
			except os.Error:
				sys.stderr.write("could not enter directory "+curr_element_path+"!\n")

			try:
				sys.stdout.write("  attempting command\n")
				subprocess.call([spcommand],shell=True)
			except subprocess.Error:
				sys.stderr.write("  command "+spcommand+" failed\n")

			sys.stdout.write("exiting directory "+curr_element_path+"\n")
			sys.stdout.write("entering directory "+root_path+"\n")
			try:
				os.chdir(root_path)
			except os.Error:
				sys.stderr.write("could not enter root directory "+root_path+"!\n")
				sys.stderr.write("exiting program "+args[1]+"...\n")
				sys.exit()

if __name__ == "__main__":
	if (check_args(sys.argv)):
		main(sys.argv)
	else:
		sys.exit()
