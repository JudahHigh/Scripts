#!/usr/bin/python

import os
import sys
import re
import linecache
import numpy as np

def convertStr(s):
   try:
      ret = int(s)
   except ValueError:
      ret = float(s)
   return ret

if len(sys.argv)==1:
	print "\nNo G09 log file specified..."
	print "Now exiting...\n"
	sys.exit()

if os.path.exists("./"+sys.argv[1])==False:
	print "\n"+sys.argv[1]+" does not exists in current directory"
	print "Now exiting...\n"
	sys.exit()

datafile=sys.argv[1]
numlines=sum(1 for line in open(datafile))
energy=[]
f=[]
excitationCount=-1
xyCount=-1

xy=np.zeros(100*100)
xy.shape=100,100
xory=np.zeros(100*100)
xory.shape=100,100
occ=np.zeros(100*100)
occ.shape=100,100
vir=np.zeros(100*100)
vir.shape=100,100
index=np.zeros(100*100)
index.shape=100,100

nElectrons=0
homo=0
lumo=0

print "\nReading in excitation data from \""+sys.argv[1]+"\""
for i in range(1,numlines+1):
	line=linecache.getline(datafile,i).strip()
	if "Leave Link  914" in line:
		break
	if "alpha electrons" in line:
		line=line.split()
		nElectrons=convertStr(line[0])*2
		homo=nElectrons/2
		lumo=homo+1
	if "Excited State" in line:
		xyCount=-1
		excitationCount+=1
		line=line.split()
		energy.append(line[6])
		f.append(line[8].split('=')[1])
	if "->" in line or "<-" in line:
		xyCount+=1
		line=line.split()
		xy[excitationCount,xyCount]=2*(convertStr(line[3])**2)*100
		if line[1]=="->":
			xory[excitationCount,xyCount]=1
		elif line[1]=="<-":
			xory[excitationCount,xyCount]=-1
		occ[excitationCount,xyCount]=convertStr(line[0])
		vir[excitationCount,xyCount]=convertStr(line[2])

#Sorts all orbital contributions in descending order
for i in range(100):
	indexes={}
	occrow=[]
	virrow=[]
	xoryrow=[]
	for j in range(100):
		indexes[xy[i,j]]=j
	xy[i,:]=sorted(xy[i,:],reverse=True)
	for j in range(100):
		occrow.append(occ[i,indexes[xy[i,j]]])
		virrow.append(vir[i,indexes[xy[i,j]]])
		xoryrow.append(xory[i,indexes[xy[i,j]]])
	occ[i,:]=occrow[:]
	vir[i,:]=virrow[:]
	xory[i,:]=xoryrow[:]

output=open(sys.argv[2]+"-excitations.txt","w")
output.write("lambda;f;orbital contributions to excitation\n")
for i in range(len(energy)):
	transitionStr=""
	transitionStr=energy[i]+";"+f[i]+";"
	for j in range(len(xy[i,:])):
		if xory[i,j]==0.0:
			continue
		if xory[i,j]!=0.0 and j!=0:
			transitionStr=transitionStr+", "
		if occ[i,j]==homo:
			transitionStr=transitionStr+"H"
		if occ[i,j]!=homo:
			transitionStr=transitionStr+"H-"+str(int(homo-occ[i,j]))
		if xory[i,j]==1:
			transitionStr=transitionStr+"-->"
		if xory[i,j]==-1:
			transitionStr=transitionStr+"<--"
		if vir[i,j]==lumo:
			transitionStr=transitionStr+"L"+"("+"{:.2f}%".format(xy[i,j])+")"
		if vir[i,j]!=lumo:
			transitionStr=transitionStr+"L+"+str(int(vir[i,j]-lumo))+"("+"{:.2f}%".format(xy[i,j])+")"
	transitionStr=transitionStr+"\n"
	output.write(transitionStr)
output.close()

print "Organized data written to \"excitations.txt\""
print "Follow steps to check generated data"
print "  - open \"excitations.txt\" in microsoft excel"
print "  - check the Delimited box and click next"
print "  - check the \"Semicolon\" in the delimeter box,\n      uncheck the \"Tab\" and click next"
print "  - highlight the orbital contirubution section\n      in \"data preview\" and then select \"Text\"\n      within \"Column data format\" box"
print "  - click finish"
print "  - highlight and copy data into microsoft\n      word as table and format"
print "now exiting...\n"


