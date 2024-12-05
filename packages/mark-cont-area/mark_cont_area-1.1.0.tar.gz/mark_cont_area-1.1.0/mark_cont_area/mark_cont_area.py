import numpy as np

def dfs(grid, row, col, visited, label):
    # 定义八个方向的移动
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    # 标记当前位置已访问
    visited[row][col] = True
    
    # 标记当前位置为指定标签
    grid[row][col] = label
    
    # 初始化当前连通区域中1的数量
    count = 1
    
    # 遍历当前位置的八个相邻位置
    for dr, dc in directions:
        r = row + dr
        c = col + dc
        
        # 检查相邻位置是否有效，并且是未访问过的1
        if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r][c] == 1 and not visited[r][c]:
            # 递归调用DFS
            count += dfs(grid, r, c, visited, label)
    
    return count

def mark_cont_area(grid, min_points):
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    label = 100  # 需要大于1，且下面也要跟随变化
    
    # 遍历整个矩阵
    for i in range(rows):
        for j in range(cols):
            # 如果当前位置是未访问过的1，则进行DFS，并标记连续区域
            if grid[i][j] == 1 and not visited[i][j]:
                ones_count = dfs(grid, i, j, visited, label)
                if ones_count < min_points:
                    # 连通区域中1的数量少于阈值，将其标记为0
                    grid[grid == label] = 0
                label += 1
    
    # 重新分配标签，使得标签按照间隔为1的自然数排列
    new_label = 1
    for i in range(100, label):
        if np.any(grid == i):
            grid[grid == i] = new_label
            new_label += 1
    
    return grid
