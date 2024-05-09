#!/public1/home/sch0149/deepmd-kit/bin/python

import numpy as np
from collections import Counter

def generate_matrix(elements, P_list, m):
    # 归一化概率列表以确保总和为1
    P_list = np.array(P_list)
    P_list = P_list / P_list.sum()

    # 检查元素和概率列表的长度是否匹配
    if len(elements) != len(P_list):
        raise ValueError("The length of elements and P_list must be the same.")
    
    # 生成元素列表
    matrix = []
    for element, probability in zip(elements, P_list):
        count = round(probability * m)
        matrix.extend([element] * count)

    # 调整大小以匹配m
    while len(matrix) < m:
        matrix.append(np.random.choice(elements, p=P_list))
    while len(matrix) > m:
        matrix.pop()

    # 打乱列表
    np.random.shuffle(matrix)

    # 转换为numpy数组
    matrix = np.array(matrix)
    return matrix


if __name__ == "__main__":
  # 示例用法
  elements = ["Mo", "Cr", "Mn", "V", "Zn"]
  P_list = [0.1, 0.2, 0.3, 0.25, 0.15]
  m = 41

  matrix = generate_matrix(elements, P_list, m)
  print(matrix)

  # 可选：验证元素计数
  element_counts = Counter(matrix)
  print(element_counts)

