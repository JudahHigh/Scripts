import os
import sys
import re
import linecache
from numpy import array, cross, pi, cos, arccos as acos, zeros, sqrt
from time import time

class DihedralGeometryError(Exception): pass
class AngleGeometryError(Exception): pass

###################################################################
#																						#
# This script takes in a .xyz file produced from dftb+ and 			#
# generates a file called 'dihedral.dat' that maps the change in	#
# the dihedral angle through an MD simulation for 4 specified 		#
# atoms.  To run the script the user must take the following		#
# steps.																				#
#																						#
#  (I) run the script in the same directory as the '.xyz' file.   #
#			user must invoke the following commands,						#
#																						#
#		python mddad.py [FILENAME] [STEPS] atom1 atom2 atom3 atom4	#
#																						#
###################################################################

# this is a function that converts a sting to an integer or float if int
# doesn't work.
def convertStr(s):
	try:
		ret = int(s)
	except ValueError:
		ret = float(s)
	return ret

def getPt(line):
	vout=zeros(3,dtype='float64') # VECTOR A
	line=line.strip().split()
	for i in range(3):
		vout[i]=convertStr(line[i+1])
	return vout

def getdihedral(a,b,c,d):
	v1 = getNormedVector(a,b)
	v2 = getNormedVector(b,c)
	v3 = getNormedVector(c,d)
	v1=array(v1)
	v2=array(v2)
	v3=array(v3)
	v1v2 = cross(v1,v2)
	v2v3 = cross(v2,v3)
	return getAngle(v1v2,v2v3)

def getNormedVector(a,b):
	abdiff=b-a
	norm_abdiff=linalg.norm(abdiff)
	unit_abdiff=abdiff/norm_abdiff
	return unit_abdiff

def getAngle(a,b):
	norm_a=linalg.norm(a)
	b_trans=b.T
	norm_b=linalg.norm(b)
	unit_a=a/norm_a
	unit_bT=b_trans/norm_b
	ab=dot(unit_a,unit_bT)
	arccos_ab_rad=arccos(ab)
	arccos_ab_deg=rad2deg(arccos_ab_rad)
	return arccos_ab_deg

def NEWgetAllAngles(filename,case,atoms,begn,endn,ROUND_ERROR):
	for i in range(endn-begn):
		line=linecache.getline(filename, begn+i)
		if 'MD iter:' in line:
			v=[]
			for j in range(len(atoms)):
				v.append(getPt(linecache.getline(filename, begn+i+atoms[j]).strip()))
			ANGLES[((i+1+natoms)/(natoms+2))-1]=intCoord(case,v)

def norm(a):
	return sqrt(sum((a*a).flat))

def fix_rounding_error(x,ROUND_ERROR):
	if -ROUND_ERROR < x < 0:
		return 0
	elif 1 < x < 1+ROUND_ERROR:
		return 1
#	elif x<=-1.0:
#		return x+ROUND_ERROR
	else:
		return x

def scalar(v1,v2):
	return sum(v1*v2)

def angle(v1,v2):
	length_product = norm(v1)*norm(v2)
	if length_product == 0:
		raise AngleGeometryError(\
		"Cannot calculate angle for vectors with length zero")
	cosine = scalar(v1,v2)/length_product
	angle = acos(fix_rounding_error(cosine,ROUND_ERROR))
	return angle

def calc_angle(vec1,vec2,vec3):
	if len(vec1) == 3:
		v1, v2, v3 = map(create_vector,[vec1,vec2,vec3])
	else:
		v1, v2, v3 = map(create_vector2d,[vec1,vec2,vec3])
	v12 = v2 - v1
	v23 = v2 - v3
	return angle(v12, v23)

def create_vector2d(vec):
	return array([vec[0],vec[1]])
	 

def create_vector(vec):
	return array([vec[0],vec[1],vec[2]])
	 
def create_vectors(v):
	return map(create_vector,v)

def intCoord(case,v):
	if case==4:
		# create array instances.
		v1,v2,v3,v4 =create_vectors(v)
		all_vecs = [v1,v2,v3,v4]
	
		# rule out that two of the atoms are identical
		# except the first and last, which may be.
		for i in range(len(v)-1):
			for j in range(i+1,len(v)):
				if i>0 or j<3: # exclude the (1,4) pair
					equals = v[i]==v[j]
					if equals.all():
						raise DihedralGeometryError(\
							"Vectors #%i and #%i may not be identical!"%(i,j))

		# calculate vectors representing bonds
		v12 = v2-v1
		v23 = v3-v2
		v34 = v4-v3
	
		# calculate vectors perpendicular to the bonds
		normal1 = cross(v12,v23)
		normal2 = cross(v23,v34)
	
		# check for linearity
		if norm(normal1) == 0 or norm(normal2)== 0:
			raise DihedralGeometryError(\
			"Vectors are in one line; cannot calculate normals!")

		# normalize them to length 1.0
		normal1 = normal1/norm(normal1)
		normal2 = normal2/norm(normal2)
	
		# calculate torsion and convert to degrees
		torsion = angle(normal1,normal2) * 180.0/pi
	
		# take into account the determinant
		# (the determinant is a scalar value distinguishing
		# between clockwise and counter-clockwise torsion.
		if scalar(normal1,v34) >= 0:
			return torsion
		else:
			torsion = 360-torsion
			if torsion == 360: torsion = 0.0
			return torsion

ROUND_ERROR = 1e-14

if len(sys.argv)<4:
	print "Need .xyz file, nsteps, and at least 1 atom"
	sys.exit()
if len(sys.argv)==4:
	print "Obtaining coords of atom ",sys.argv[3]
	case=1
if len(sys.argv)==5:
	print "Obtaining distances between atom ",sys.argv[3]," and ",sys.argv[4]
	case=2
if len(sys.argv)==6:
	print "Obtaining angles defined by atoms ",sys.argv[3]," ",sys.argv[4]," ",sys.argv[5]
	case=3
if len(sys.argv)==7:
	print "Obtaining dihedral angles defined by atoms ",sys.argv[3]," ",sys.argv[4]," ",sys.argv[5]," ",sys.argv[6]
	case=4

if case==1:
	atoms=[int(sys.argv[3])]
if case==2:
	atoms=[int(sys.argv[3]),int(sys.argv[4])]
if case==3:
	atoms=[int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])]
if case==4:
	atoms=[int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6])]
STEPS=int(sys.argv[2])
FILENAME=sys.argv[1]

n=STEPS
natoms=convertStr(linecache.getline(FILENAME, 1).strip())
begn=0
endn=(STEPS*natoms)+(2*STEPS)

t1=time()
ANGLES=zeros(STEPS,dtype='float64')
NEWgetAllAngles(FILENAME,case,atoms,begn,endn,ROUND_ERROR)
gnuplotfile=open('internal_coords.dat','w')
for i in range(len(ANGLES)):
	gnuplotfile.write('{:10d}	{:13.8f}\n'.format(i,ANGLES[i]))
t2=time()
print t2-t1
