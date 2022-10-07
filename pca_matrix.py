import numpy as np
from math import log10, floor
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

    root_path = 'E:\\SRTP\\part\\'
    num = 150

    pca_matrix = list()
    for i in range(num):
        if i == 0:
            dir_name = '000'
        else:
            dir_name = (2 - int(log10(i))) * '0' + repr(i)
        print(dir_name)
        file_name = root_path + dir_name + '\\' + 'pointcloud.npz'
        bool_arr = PointRasterize(file_name, N = 8)
        pca_matrix.append(bool_arr)
    
    WritePCAMatrix(pca_matrix)


if __name__ == '__main__':
    main()