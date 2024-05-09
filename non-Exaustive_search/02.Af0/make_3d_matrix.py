#!/public1/home/sch0149/deepmd-kit/bin/python

import sys
sys.path.append("/public1/home/sch0149/script/mimic_suite/")
sys.path.append("/public1/home/sch0149/script/ase_based_constraint_opt_suite/")

from ase.io import write
from ase.io import read
from ase import neighborlist
from ase import geometry
import numpy as np
from mimic_functions import *
from project_to_grid_functions import *
import os
import time
import re


fs=os.listdir('./')
fs.sort()
fs_aftxt=[]
for f in fs:
    if f.endswith('_Af_matrix.txt'):
        fs_aftxt.append(f)


Af_matrix_3d=[]

for f_aftxt in fs_aftxt:

  Af_matrix = np.loadtxt(f_aftxt)

  Af_matrix_3d.append(Af_matrix)

Af_matrix_3d = np.array(Af_matrix_3d)

print(Af_matrix_3d.shape)
