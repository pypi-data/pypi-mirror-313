import numpy as np

def fill_only1gap(matrix):
    rows, cols = matrix.shape
    helper_matrix = np.zeros((rows, cols), dtype=int)

    # 遍历原始矩阵
    for i in range(rows):
        for j in range(cols):
            # 检查左右相邻位置
            if j > 0 and j < cols - 1 and matrix[i][j-1] == 1 and matrix[i][j+1] == 1:
                helper_matrix[i][j] = 1
            # 检查上下相邻位置
            elif i > 0 and i < rows - 1 and matrix[i-1][j] == 1 and matrix[i+1][j] == 1:
                helper_matrix[i][j] = 1
    
    # 将原始矩阵与辅助矩阵逐元素相加
    result_matrix = matrix + helper_matrix
    
    # 将结果矩阵中大于1的元素设为1
    result_matrix[result_matrix > 1] = 1
    
    return result_matrix
