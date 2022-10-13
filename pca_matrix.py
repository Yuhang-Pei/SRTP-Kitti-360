import numpy as np
import os
from math import floor
from utility import Standardize

def PointRasterize(file_name, N: int):
    points = np.load(file_name)['points']
    std_points = Standardize(points)

    bool_arr = [0] * (N ** 3)    
    for i in range(len(points)):
        i_x = floor(N * (std_points[i][0] + 0.6) / 1.2)
        i_y = floor(N * (std_points[i][1] + 0.6) / 1.2)
        i_z = floor(N * (std_points[i][2] + 0.6) / 1.2)
        bool_arr[i_x + N * i_y + N * N * i_z] = 1

    return bool_arr

def WritePCAMatrix(pca_matrix: list):
    pca_matrix_file = open('pca_matrix.dat', 'w')
    for line in pca_matrix:
        pca_matrix_file.writelines(''.join(map(str, line)) + "\n")
    pca_matrix_file.close()

def main():
    # 此处需要相应函数接口，获取root_path和模型数目num
    # 此处的root_path和num已经固定了

    root_path = './model/'
    num = 400

    pca_matrix = list()
    dirs = os.listdir(root_path)
    for dir in dirs:
        file = root_path + dir + '/pointcloud.npz'
        print(file)
        bool_arr = PointRasterize(file, N = 8)
        pca_matrix.append(bool_arr)
    
    WritePCAMatrix(pca_matrix)


if __name__ == '__main__':
    main()