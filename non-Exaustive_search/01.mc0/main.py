#!/public1/home/sch0149/deepmd-kit/bin/python

import sys
from ase.io import write
from ase.io import read
from ase import neighborlist
from ase import geometry
import numpy as np
import os
import time
import re
import shutil
import random
import subprocess

from math_functions import *
from file_operation import *

if not os.path.exists('uniq_element_list'):
  print("use get_elelist_from_pb.py f_dp first")
  sys.exit()  


input_dic = parse_input_file('input.parameters')

elements_pool = input_dic['elements_pool'].split(" ")
P_list = input_dic['P_list'].split(" ")
P_list = [float(x) for x in P_list]
print("P_list=",P_list)

f_dp = input_dic['f_dp']
nelement_chose = int(input_dic['nelement_chose'])
f_str = input_dic['f_str']

work_dir = input_dic['work_dir']

mkdir_if_not_exists(work_dir)

sub_script = input_dic['opt_script']

atoms=read(f_str)

n_loop_time = int(input_dic['n_loop_time'])

for loop_time in range(n_loop_time):
  print("////loop_time=",loop_time,"/////////////////")

  selected_elements = random.sample(elements_pool, nelement_chose)
  natm = len(atoms)

  atoms_HEA = atoms.copy()
  eles = generate_matrix(selected_elements, P_list, natm) 
  atoms_HEA.set_chemical_symbols(eles)

  prefix = '_'.join(selected_elements)
  
  if not os.path.exists('./material_lmp/'+prefix):
    mkdir('./material_lmp/'+prefix)
    write('./material_lmp/'+prefix+"/blank.xyz",atoms_HEA)

sub_script = input_dic['opt_script'] 
command = [sub_script]

print("shell command =", command)

# 执行命令，并通过input参数传递输入
with open(sub_script+'.out','w') as output_file:
  subprocess.run(command, text=True, stdout=output_file, stderr=subprocess.PIPE)

