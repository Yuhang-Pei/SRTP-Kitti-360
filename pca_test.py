import numpy as np
from math import floor
from utility import load_obj
from utility import Standardize, Rotate, PointsToObj

'''
    @brief: Read the original point data from the text file
            (Notice that the data from KITTI-360 are in form of .txt)
    @param file_name: the name of the text file
'''
def ReadPCATestData(file_name):
    test_data = list()
    with open(file = file_name, mode = 'r') as file:
        for line in file:
            tmp = line.split()
            test_data.append([float(x) for x in tmp])
    
    return test_data


'''
    @brief: Rasterize the point data into bool array data
    @param points: the original data of points
    @param N: the scale of rasterization
'''
def Rasterize(points, N: int):
    std_points = Standardize(points)

    bool_arr = [0] * (N ** 3)
    for i in range(len(points)):
        i_x = floor(N * (std_points[i][0] + 0.6) / 1.2)
        i_y = floor(N * (std_points[i][1] + 0.6) / 1.2)
        i_z = floor(N * (std_points[i][2] + 0.6) / 1.2)
        bool_arr[i_x + N * i_y + N * N * i_z] = 1

    return bool_arr


#-----------------------------------------------------------------------------
# Find the most similar model by iterate all possibilities 

import heapq

def FindMostSimilarModel1(train_result: list, test_result: list, index = 0):
    min_dist = 999999999999
    min_index = cur_index = 0
    for row in train_result:
        dist = np.linalg.norm(row - test_result[index])
        if dist < min_dist:
            min_dist = dist
            min_index = cur_index
        cur_index = cur_index + 1
    return min_index


def FindMostSimilarModel(train_result: list, test_result: list, index = 0, n = 1):
    # When n is 1, it is more efficient to iterate directly rather than using priority queue
    if n == 1:
        return FindMostSimilarModel1(train_result, test_result, index)
    
    # When n is greater than 1, use priority queue
    tuple_heap = list()
    cur_index = 0
    for row in train_result:
        cur_dist = np.linalg.norm(row - test_result[index])
        cur_tuple = (cur_dist, cur_index)
        heapq.heappush(tuple_heap, cur_tuple)
        cur_index = cur_index + 1
    return heapq.nsmallest(n, tuple_heap)


#-----------------------------------------------------------------------------

def main():
    # read testing data
    point_test_data = ReadPCATestData('2.txt')
    point_test_data = Rotate(point_test_data, [0, 0, -0.4343581680770375])
    PointsToObj('2.obj', Standardize(point_test_data))  # for test
    pca_test_data = Rasterize(point_test_data, 8)
    pca_test_data = np.array([pca_test_data])

    # load pca object
    pca = load_obj('pca')

    # perform pca transformation on testing data
    pca_test_result = pca.transform(pca_test_data)

    # read training data
    pca_train_result = load_obj('pca_train_result')

    # find the most similar model
    print(FindMostSimilarModel(pca_train_result, pca_test_result, n = 3))


if __name__ == '__main__':
    main()