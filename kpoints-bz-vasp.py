from ase.structure import bulk
from ase.dft.kpoints import *
from ase.io import *
import numpy as np
import os
from ase.calculators.vasp import Vasp
from ase.lattice.spacegroup import crystal

# Read input parameters
crystal = read('POSCAR',index=-1,format='vasp')
lattice = raw_input('Lattice type [cubic/fcc/bcc/hexagonal/tetragonal/orthorhombic] ')
special_points = raw_input('Which special points do you want to sample (in order) ')
sample = raw_input('How many points do you want to sample ')

# Set up special points lattices
points = ibz_points[lattice]
special = np.zeros(shape=(len(special_points.split()),3)) 


# Define KPOINTS for special points
i = 0
for point in special_points.split():
 special[i,:] = points[point]
 i = i + 1
print special
kpoints, x, X = get_bandpath(special,crystal.cell,int(sample))

#Dirty printing of the KPOINTS file
f_handle = file('KPOINTS', 'a')
f_handle_b = file('tmp', 'w')
f_handle.write('KPOINTS FILE\n')
f_handle.write(str(len(kpoints)))
f_handle.write('\n')
f_handle.write('Reciprocal \n')
np.savetxt(f_handle_b, kpoints)
f_handle_b.close()
f_handle.close()
os.system('awk \'{printf \"%s %10.8f %10.8f %10.8f %5.2f \\n\","  ",$1,$2,$3,1}\' tmp >> KPOINTS')
os.system('rm tmp')
# Define the band structure calculation
