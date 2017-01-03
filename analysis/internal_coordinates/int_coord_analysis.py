import os
import sys
import re
import copy

def gen_connectivity(ifname):
	nblanks=0
	connect=[]
	with open(ifname,'r') as ifstream:
		for line in ifstream:
			if ( nblanks >= 3 ):
				if ( line != "\n" ):
					line=line.strip().split()
					connect.append(line[0])
					linelen=len(line)
					for i in range(1,linelen):
						if ( i % 2 != 0 ):
							connect.append(int(line[i]))
			if ( line == "\n" ):
				nblanks+=1

	bonds={}
	value=[]
	set_kv=False
	for i in range(len(connect)):
		if (type(connect[i]) == str):
			if ( i == 0 ):
				curr_key = connect[i]
			if ( i != 0 ):
				bonds[int(curr_key)] = value
				value = []
				curr_key = connect[i]
		if (type(connect[i]) == int):
			value.append(connect[i])
		if ( i == len(connect)-1 ) and ( type(connect[i]) == str ):
			curr_key = connect[i]
			bonds[int(curr_key)] = []
	return bonds

def gen_bond_arr(connect):
	bonds=[]
	for k, v in connect.items():
		if ( len(v) > 0):
			for atom in range(len(v)):
				bonds.append(k)
				bonds.append(v[atom])
	return bonds

def gen_angle_arr(connect,natoms):
	angles=[]
	loop_atoms = [-1 for i in range(natoms)]
	for atom2, v in connect.items():
		if ( len(v) > 0 ):
			if ( len(v) >= 2 ):
				for i in range(len(v)):
					for j in range(i,len(v)):
						if ( i != j ):
							atom1 = v[i]
							atom3 = v[j]
							angles.extend((atom1,atom2,atom3))
			for i in range(len(v)):
				bak_atom2 = atom2
				atom1 = atom2
				atom2 = v[i]
				if ( len(connect[atom2]) > 0 ):
					for j in range(len(connect[atom2])):
						atom3 = connect[atom2][j]
						angles.extend((atom1,atom2,atom3))
				atom2 = bak_atom2
		for i in range(len(v)):
			loop_atoms[v[i]-1]+=1
	for i in range(len(loop_atoms)):
		if ( loop_atoms[i] == 1 ):
			loop_atom=i+1
			loop_angle=[loop_atom]
			for k,v in connect.items():
				if ( loop_atom in connect[k] ):
					loop_angle.append(k)
				if ( len(loop_angle)==3):
					b = loop_angle[0]
					loop_angle[0] = loop_angle[1]
					loop_angle[1] = b
					angles.extend((loop_angle[0],loop_angle[1],loop_angle[2]))
					loop_angle=[loop_atom]
	return angles

def gen_dihedral_arr(connect,natoms):
	dihedrals=[]
	loop_atoms = [-1 for i in range(natoms)]
	for k,v in connect.items():
		for i in range(len(v)):
			loop_atoms[v[i]-1]+=1
	for i in range(len(loop_atoms)):
		if ( loop_atoms[i] == 1 ):
			loop_atom = i+1
			for k,v in connect.items():
				if ( loop_atom in connect[k] ):
					connect[loop_atom].append(k)
	print connect

	search_keys = []
	for k,v in connect.items():
		switch_list = [k] + connect[k]
		for switch in range(len(switch_list)):
			temp = []
			n_k = switch_list[switch]
			temp.append(n_k)
			n_dict_key = 0
			for i in range(len(switch_list)):
				if ( switch_list[i] != n_k ):
					n_dict_key = switch_list[i]
					break
			temp.append(n_dict_key)
			search_keys.append(temp)
	connect[0]=[]
	print search_keys
	somefile=open('somefile.log','w')
	for i in range(len(search_keys)):
		dihedral=[]
		dihedral.append(search_keys[i][0])
		b=search_keys[i][1]

		n_tabs=0
	 	nr = 0
		rec_dict_loop(connect,b,dihedral,n_tabs,nr,somefile) # recursively get all possible dihedrals
	dihedrals=[]
	temp_list=[]
	somefile.close()
	with open('somefile.log','r') as somefile:
		for line in somefile:
			temp_list.append(line.strip())
	for i in range(len(temp_list)):
		if (len(temp_list[i]) == 7):
			if ( not temp_list[i] in dihedrals ):
				temp2=temp_list[i].split()
				for j in range(len(temp2)):
					curr_el=temp2[j]
					for k in range(len(temp2)):
						if ( int(curr_el) == int(temp2[k]) ):
							circular=True
							break
				if ( not circular ):
					dihedrals.append(temp_list[i])
				circular = False
	somefile.close()
	os.remove('./somefile.log')


	dcopy={}
	for i in range(len(dihedrals)):
		dcopy[dihedrals[i]]=copy.deepcopy(dihedrals[i])
	for i in range(len(dihedrals)):

		temp=""
		for j in range(len(dihedrals[i])):
			temp=temp+dihedrals[i][len(dihedrals[i])-1-j]

		for j in range(len(dihedrals)):
			if ( temp in dcopy.values() ):
				del dcopy[temp]
	dcopylist=[]
	for k,v in dcopy.items():
		dcopylist.append(k)
		del dcopy[k]
	dcopylist=list(set(dcopylist))
	dihedrals=[]
	for i in range(len(dcopylist)):
		temp=dcopylist[i].split()
		for j in range(len(temp)):
			dihedrals.append(int(temp[j]))
	print dcopylist
	
	

def rec_dict_loop(m_dict,m_k,m_list,n,nr,somefile):
	nr+=1
	n+=3
	m_list.append(m_k)
	if ( len(m_dict[m_k]) > 0 ) and ( len(m_list) < 4 ):
		for i in range(len(m_dict[m_k])):
			n_k = m_dict[m_k][i]
			rec_dict_loop(m_dict,n_k,m_list,n,nr,somefile)
			m_list.pop(len(m_list)-1)
	else:
		for i in range(len(m_list)):
			somefile.write(str(m_list[i])+" ")
		somefile.write("\n")
		nr-=1
		n-=1
		return m_list
	return m_list
			
	

ifname=sys.argv[1]
connect = gen_connectivity(ifname)
print "CONNECTIVITY"
print connect

natoms=len(connect)
print "\nnatoms = ",natoms

bonds=gen_bond_arr(connect)
print "\nBONDS"
print bonds, len(bonds), len(bonds)/2
angles=gen_angle_arr(connect,natoms)
print "\nANGLES"
print angles, len(angles), len(angles)/3
print "\nDIHEDRALS"
gen_dihedral_arr(connect,natoms)



