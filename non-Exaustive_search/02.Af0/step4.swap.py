#!/public1/home/sch0149/deepmd-kit/bin/python

import numpy as np
import random

def swap_rows_cols(matrix, idx1, idx2):
  # Swap rows
  matrix[[idx1, idx2], :] = matrix[[idx2, idx1], :]
  # Swap columns
  matrix[:, [idx1, idx2]] = matrix[:, [idx2, idx1]]
  return matrix

def average_top_three(numbers):
    # Sort the numbers in descending order
    sorted_numbers = sorted(numbers, reverse=True)
    
    # Select the top three numbers
    top_three = sorted_numbers[:5]
    
    # Calculate the average of the top three numbers
    average = sum(top_three) / len(top_three)
    return average


def swap_elements(array, i, j):
    # Swap the elements at indices i and j
    array[i], array[j] = array[j], array[i]
    return array



ele_list = np.loadtxt('ele_list',dtype=str)

matrix=np.loadtxt("Af_matrix.txt")

for iter_step in range(2000):

  print("----------",iter_step,"-------------")
  #
  random_numbers = random.sample(range(matrix.shape[0]), 2)

  #check
  #比较最大的前三个数的平均值
  larger_index = max(random_numbers)
  smaller_index = min(random_numbers) 

  average1 = average_top_three(matrix[larger_index]) 

  average2 = average_top_three(matrix[smaller_index])


  #large_index should have smaller value
  if average1 > average2:
    
    print("average of larger index",ele_list[larger_index],"is larger than average of smaller index ", ele_list[smaller_index],",(",average1,">",average2,"), swap then")
    matrix = swap_rows_cols(matrix, larger_index, smaller_index)
    ele_list = swap_elements(ele_list,larger_index, smaller_index)    

  else:

    print("average of larger index",ele_list[larger_index],"is sammler than average of smaller index ", ele_list[smaller_index],",(",average1,"<",average2,"), no need to swap")
        

np.savetxt('final_Af_matrix.txt',matrix,fmt='%.5f')
np.savetxt('final_ele_list',ele_list,fmt='%s') 

