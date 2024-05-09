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

def initialize_matrix_dict(matrix):
  
  #
  nraw    = matrix.shape[0]
  ncolumn = matrix.shape[1]

  matrix_dict = {(i, j): 0 for i in range(nraw) for j in range(ncolumn)}

  return matrix_dict


def get_nraw_ncolumn_from_matrix_dic(matrix_dict):

  #
  max_i, max_j = 0, 0

  # Iterate over the keys of the dictionary to find the maximum values
  #print("matrix_dict.keys()=",matrix_dict.keys())
  for (i, j) in matrix_dict.keys():
    #print("i,j=",i,j)
    if i > max_i:
        max_i = i
    if j > max_j:
        max_j = j

  nraw    = max_i+1
  ncolumn = max_j+1

  return nraw,ncolumn

def initialize_matrix_dict_all_data(nraw,ncolumn):
  '''
  matrix_dict_all_data保存有每一次Af，对于每一个Af，都是一个Af阵列
  '''
  #
  #nraw    = matrix.shape[0]
  #ncolumn = matrix.shape[1]

  matrix_dict_all_data = {(i, j): [] for i in range(nraw) for j in range(ncolumn)}

  return matrix_dict_all_data


def merge_matrix_into_matrix_dict_all_data(matrix_dict_all_data, matrix_dict):
  '''
  将matrix append到matrix_dict_all_data
  '''
  nraw,ncolumn = get_nraw_ncolumn_from_matrix_dic(matrix_dict)
  print("nraw,ncolumn =",nraw,ncolumn )

  new_matrix_dict_all_data = {(i, j): list(np.append(matrix_dict_all_data[(i,j)],matrix_dict[(i,j)])) for i in range(nraw) for j in range(ncolumn)}
  
  return new_matrix_dict_all_data


def make_matrix_dict_from_matrix_dict_all_data(matrix_dict_all_data):
  '''
  通过对于matrix_dict_all_data求平均获取matrix_dict。如果为Af为[]，则将其操作为0
  '''

  #
  nraw,ncolumn = get_nraw_ncolumn_from_matrix_dic(matrix_dict_all_data)
  print("nraw,ncolumn=",nraw,ncolumn)

  matrix_dict = {}

  for i in range(nraw):
    for j in range(ncolumn):

      if len(matrix_dict_all_data[(i,j)])==0 :  # if matrix_dict_all_data[(i,j)]==[]
        matrix_dict[(i, j)] = 0
      else:
        matrix_dict[(i, j)] = np.mean(matrix_dict_all_data[(i,j)])


  return matrix_dict


def convert_Af_matrix_to_Af_matrix_dict(Af_matrix):
 
  Af_matrix_dict = {(i, j): Af_matrix[i][j] for i in range(Af_matrix.shape[0]) for j in range(Af_matrix.shape[1])}

  return Af_matrix_dict
 
#
fs=os.listdir('./')
fs.sort()
fs_aftxt=[]
for f in fs:
    if f.endswith('_Af_matrix.txt'):
        fs_aftxt.append(f)

#step 1
Af_matrix_3d=[]

for f_aftxt in fs_aftxt:

  Af_matrix = np.loadtxt(f_aftxt)

  Af_matrix_3d.append(Af_matrix)

Af_matrix_3d = np.array(Af_matrix_3d)

#step 2

#1.initialize Af_matrixs_not_yet_discussed
Af_matrixs_not_yet_discussed = Af_matrix_3d

#2.initialize final_Af_matrix_dict_all_data
Af_matrix0 = Af_matrixs_not_yet_discussed[0]
final_Af_matrix_dict_all_data = initialize_matrix_dict_all_data(Af_matrix0.shape[0],Af_matrix0.shape[1])

print("Af_matrix0=",Af_matrix0)
print("final_Af_matrix_dict_all_data=",final_Af_matrix_dict_all_data)

Af_matrix0_dict = {(i, j): Af_matrix0[i][j] for i in range(Af_matrix0.shape[0]) for j in range(Af_matrix0.shape[1])}
print("Af_matrix0_dict=",Af_matrix0_dict)

new_final_Af_matrix_dict_all_data = merge_matrix_into_matrix_dict_all_data(final_Af_matrix_dict_all_data, Af_matrix0_dict)
final_Af_matrix_dict_all_data = new_final_Af_matrix_dict_all_data
print("final_Af_matrix_dict_all_data",final_Af_matrix_dict_all_data)

#循环退出条件：所有的矩阵都讨论完毕 len(Af_matrixs_not_yet_discussed) = 0
while len(Af_matrixs_not_yet_discussed) !=0:
 
  #initialize final_Af_matrix_dict from final_Af_matrix_dict_all_data 
  final_Af_matrix_dict = make_matrix_dict_from_matrix_dict_all_data(final_Af_matrix_dict_all_data)  
  #print("final_Af_matrix_dict",final_Af_matrix_dict)

  #2.1 refresh the non_zero_indices of Af_matrixs_not_yet_discussed
  non_zero_indices = [key for key, value in final_Af_matrix_dict.items() if value != 0]
  
  #2.2 find any of Af_matrixs in Af_matrixs_not_yet_discussed that has the overlap of non_zero_indices  
  for index, Af_matrix in enumerate(Af_matrixs_not_yet_discussed):
    
    # Convert matrix to a dictionary format to simplify comparison
    Af_matrix_dict = {(i, j): Af_matrix[i][j] for i in range(Af_matrix.shape[0]) for j in range(Af_matrix.shape[1])}

    # Check for overlapping non-zero elements
    #overlap = any(Af_matrix_dict[pos] != 0 for pos in non_zero_indices)
    #print("Af_matrix_dict=",Af_matrix_dict)
    #print("non_zero_indices=",non_zero_indices)

    overlapping_indices = [pos for pos in non_zero_indices if Af_matrix_dict[pos] != 0]

    if overlapping_indices:
      #print("overlapping_indices=",overlapping_indices)
      #print(f"Found overlap in matrix at index {index}")

      # Remove the matrix from the series, next round we will not use it
      Af_matrixs_not_yet_discussed = np.delete(Af_matrixs_not_yet_discussed,index,axis=0)
      break  # Stop searching once an overlap is found

  Af_origianl  = final_Af_matrix_dict[overlapping_indices[0]]          
  Af_inserting = Af_matrix_dict[overlapping_indices[0]] 
   
  ratio_to_merge = Af_origianl/Af_inserting

  expanded_Af_matrix_dict = {(i, j): ratio_to_merge*Af_matrix[i][j] for i in range(Af_matrix.shape[0]) for j in range(Af_matrix.shape[1])}

  new_final_Af_matrix_dict_all_data = merge_matrix_into_matrix_dict_all_data(final_Af_matrix_dict_all_data, expanded_Af_matrix_dict)   

  final_Af_matrix_dict_all_data = new_final_Af_matrix_dict_all_data

  print("len(Af_matrixs_not_yet_discussed)=",len(Af_matrixs_not_yet_discussed))
  #print("final_Af_matrix_dict_all_data=",final_Af_matrix_dict_all_data)

#print("final_Af_matrix_dict_all_data=",final_Af_matrix_dict_all_data)
final_Af_matrix_dict = make_matrix_dict_from_matrix_dict_all_data(final_Af_matrix_dict_all_data)
print("final_Af_matrix_dict=",final_Af_matrix_dict)

import json
converted_dict = {str(key): value for key, value in final_Af_matrix_dict.items()}
# 将字典保存到JSON文件
with open('./final_Af_matrix.json', 'w') as f:
  json.dump(converted_dict, f)   


