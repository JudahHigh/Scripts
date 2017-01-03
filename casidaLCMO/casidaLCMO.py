#!/usr/bin/python

import os
import re
import sys

fname=sys.argv[1]
es=int(sys.argv[2])

holes=[]
electrons=[]
vals=[]

# maps the electron and hole numbers along with their values
getTransitions=False
with open(fname,'r') as fo:
	for line in fo:
		if getTransitions:
			temp=""
			try:

				# get hole MO numbers
				holes.append(int(line.strip().split()[0].split('-')[0]))

				# get electron MO numbers
				cases=['->','<-']
				for j in range(len(cases)):
					if cases[j] in line:
						linelist=line.strip().split()
						for i in range(len(linelist)):
							if (cases[j] in linelist[i]) and (len(linelist[i]) > 2) and (i==1) or (i==2):
								try:
									try:
										element=linelist[i].split(cases[j])[1]
									except IndexError:
										element=linelist[i].split(cases[j])[0]
									electrons.append(int(element))
								except ValueError:
									pass
					else:
						pass

				# get transition densites
				vals.append(abs(float(line.strip().split()[len(line.strip().split())-1])))
			except ValueError:
				getTransitions=False
				temp=line.strip()
		if "Excited State" in line:
			fes=int(line.strip().split()[2].split(':')[0])
			if fes==es:
				getTransitions=True

# calculates the lcmo coefficients
elcoef={}
hlcoef={}
for i in range(len(holes)):
	if holes[i] not in hlcoef:
		hlcoef[holes[i]]=0.0
	if electrons[i] not in elcoef:
		elcoef[electrons[i]]=0.0

for i in range(len(electrons)):
	elcoef[electrons[i]]=elcoef[electrons[i]]+2.0*(vals[i])**2.0
	hlcoef[holes[i]]=hlcoef[holes[i]]+2.0*(vals[i])**2.0

for i in range(len(elcoef)):
	elcoef[elcoef.keys()[i]]=elcoef[elcoef.keys()[i]]**0.5
	hlcoef[hlcoef.keys()[i]]=hlcoef[hlcoef.keys()[i]]**0.5

nel=(1.0/sum([a**2.0 for a in elcoef.values()]))**0.5
nhl=(1.0/sum([a**2.0 for a in hlcoef.values()]))**0.5

for i in range(len(elcoef)):
	elcoef[elcoef.keys()[i]]=nel*elcoef[elcoef.keys()[i]]
	hlcoef[hlcoef.keys()[i]]=nhl*hlcoef[hlcoef.keys()[i]]

elstring="ELECTRON LCMO :: "
hlstring="HOLE     LCMO :: "
for i in range(len(elcoef)):
	elstring=elstring+"   {:3d}   {:17.16f}".format(elcoef.keys()[i],elcoef.values()[i])
	hlstring=hlstring+"   {:3d}   {:17.16f}".format(hlcoef.keys()[i],hlcoef.values()[i])
print elstring
print hlstring

sys.exit()
		














