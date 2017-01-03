import sys
import re
import os

def get_coords_and_labels(infile):
	# initalize atom coords and id arrays
	ids=[]
	coords=[]

	# read atom ids and coords
	blank_line_count=0
	coord_line_count=0
	with open(infile,'r') as isfile:
		for line in isfile:
			if ( blank_line_count == 2 ):
				if ( coord_line_count == 0 ): # upon entering should set coord_line_count to 1
					coord_line_count+=1
					continue
				if ( coord_line_count > 0 ) and ( line != "\n" ): # first time to enter coord_line_count should equal 1
					if ( not "Tv" in line ):
						line=line.strip().split()
						ids.append(line[0])
						if ( len(line) == 4 ): # no special flags between atom id and coordinates
							for i in range(1,4):
								coords.append(line[i])
						elif ( len(line) > 4 ): # if special flags present between atom id and coordinates
							for i in reversed(range(len(line)-3,len(line))):
								coords.append(line[i])
						else:
							print "Not all x, y and z coordinates present on one or more lines in .com file..."
							sys.exit()
						coord_line_count+=1
			if ( line == "\n" ):
				blank_line_count+=1
			if ( blank_line_count == 3):
				break

	return coords,ids

def get_match_atom_list(coords_a,coords_b):
	matches=[]
	match_errors=[]
	coord_error_thresh=1*10.0**-6
	scale_factor = 1
	coord_error=0.0
	current_match=-1
	current_error=1000.0
	for i in range(len(coords_b)/3):
		for j in range(len(coords_a)/3):
			coord_error = 0.0
			for k in range(3):
				coord_error += abs( float(coords_b[i*3+k]) - float(coords_a[j*3+k]) )*scale_factor
			if (coord_error <= coord_error_thresh):
				if (coord_error <= current_error):
					current_match = j
					current_error = coord_error
				elif (coord_error == current_error):
					print "warning: atom",i,"is in master coord file multiple times... skipping atom",j
		matches.append(current_match)
		match_errors.append(current_error)
		current_match = -1
		current_error = 1000.0
	return matches,match_errors

def get_out_string(matches):
	ranges = [0]*len(matches)
	ranges[0] = 1
	range_num = 1
	for i in range(len(matches)):
		if ( i < len(matches)-1):
			if (matches[i]+1 == matches[i+1]):
				if (ranges[i] == 0):
					pass
				if (ranges[i] == 1):
					pass
			if (matches[i]+1 != matches[i+1]):
				ranges[i] = range_num
				range_num+=1
				ranges[i+1] = range_num
		if ( i == len(matches)-1 ):
			ranges[i] = range_num

## test case for debugging ##
#	ranges=[1,0,0,1,2,0,0,0,0,2,3,4,0,0,0,4,5]
#	for i in range(270):
#		ranges.append(0)
#	ranges.append(5)
#	range_num = 5

	range_num_count=0
	range_count_dict={}
	for i in range(range_num):
		for j in range(len(ranges)):
			if (ranges[j] == i+1):
				range_num_count+=1
		range_count_dict[i+1] = range_num_count
		range_num_count=0

	out_string=""
	be_switch=True
	for i in range(len(matches)):
		if (ranges[i] > 0):
			if (ranges[i] in range_count_dict.keys()):
				if (range_count_dict[ranges[i]] > 1):
					out_string += str(matches[i]+1)
					if ( i < len(matches)-1 ):
						if (be_switch):
							out_string += "-"
						if (be_switch == False):
							out_string += ","
					be_switch=not be_switch
				elif (range_count_dict[ranges[i]] == 1):
					out_string += str(matches[i]+1)+","
				else:
					pass
	return out_string

filename_a = sys.argv[1]
coords_a,labels_a = get_coords_and_labels(filename_a)

filename_b = sys.argv[2]
coords_b,labels_b = get_coords_and_labels(filename_b)

matches,errors = get_match_atom_list(coords_a,coords_b)
if (len(matches) > len(coords_b)):
	sys.stderr.write("duplicate atoms in {:s}".format(filename_a))

atom_match_range = get_out_string(matches)

print atom_match_range




