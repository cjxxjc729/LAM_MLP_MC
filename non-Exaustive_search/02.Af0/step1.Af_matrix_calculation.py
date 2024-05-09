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

def build_reflection_dict(ele_list,uniq_ele):

  reflection_dict={}
  for count,ele in enumerate(uniq_ele):

    reflection_dict[count]=list(ele_list).index(ele)


  return reflection_dict


fs=os.listdir('./')
fs.sort()
fs_xyz=[]
for f in fs:
    if f.endswith('.xyz'):
        fs_xyz.append(f)

#ele_list is the tottal type_map
ele_list=np.loadtxt('ele_list',dtype=str)


for f_xyz in fs_xyz:

  prefix=f_xyz.split('.xyz')[0]
  atoms = read(f_xyz)
  atoms_cordpref=label_cordpref_info(atoms)

  #uniq_ele is the ele in this file
  uniq_ele=atoms_cordpref['uniq_ele']
 
  #print(ele_list)
  #print(uniq_ele)

  reflection_dict = build_reflection_dict(ele_list,uniq_ele)  
  print(reflection_dict)

  Af_matrix_in_large_matrix = np.zeros((len(ele_list),len(ele_list)))

  Af_matrix=[]
  for ele in uniq_ele:
  
    indexs=[atom.index for atom in atoms if atom.symbol == ele]
    cord_ele_frac,cord_ele_pref=output_cord_ele_frac_by_atm_ids(atoms_cordpref,indexs)

    Af_matrix = np.append(Af_matrix,cord_ele_pref)

  Af_matrix = Af_matrix.reshape(-1,len(uniq_ele))
        
  for i in range(len(uniq_ele)):
    for j in range(len(uniq_ele)):
      
      reflected_i = reflection_dict[i]
      reflected_j = reflection_dict[j]

      Af_matrix_in_large_matrix[reflected_i,reflected_j]= Af_matrix[i,j]
  
  np.savetxt(prefix+'_Af_matrix.txt',Af_matrix_in_large_matrix,fmt='%.5f')


