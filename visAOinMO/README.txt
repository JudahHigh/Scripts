Title: visAOinMO.py
Author: Judah High
Status: Functional

Description: Takes in a formatted checkpoint file from Gaussian (.fchk ext)
and replaces the specified molecular orbital's coefficients with a new
vector of coefficients were all are zeroed except for those corresponding
to the user specified basis-function type which could be s,p,d,f,...

Gaussian basis functions are of the form (x**l)*(y**m)*(z**n)*exp(-a*r**2)
where l+m+n=L is the type. if L=0,1,2,3,... -> s,p,d,f,...

The MO has essentially been modified such that upon visualization using
something like PyMol or GaussView, one may inspect a given MO's s-type,
p-type, d-type, f-type, ... character. This is a useful analysis tool from
a molecular orbital theory perspective and from an atoms in molecules
perspective.

Use: User passes in (1) formatted checkpoint file, (2) MO number (1,2,3, 
... , nMO), (3) alpha or beta ('a' or 'b') and (4) the AO type (s,p,d or f
currently).

>> python visAOinMO.py benzene.fchk 1 p

yields a file benzeneNEW.fchk which may be used in a MO visualization package to
inspect the modified MO.
