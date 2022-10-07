import numpy as np
from sklearn.decomposition import PCA

def ReadPCAMatrixData(pca_matrix: list):
    with open(file = 'pca_matrix.dat', mode = 'r') as pca_matrix_file:
        while 1:
            line = pca_matrix_file.readline()
            if not line:
                break;
            l = [ord(x) - ord('0') for x in line]
            l.pop()
            pca_matrix.append(l)

def MatchingDegree(v1, v2):
    return np.linalg.norm(v1 - v2)

def PCAProcess(dimension):
    pca_matrix = list()
    ReadPCAMatrixData(pca_matrix)

    # temporarily remove the last row
    last = pca_matrix.pop()
    pca = PCA(n_components = dimension)

    # for test
    test = np.array(pca_matrix)
    pca_test = pca.fit_transform(test)
    last = np.array(last)
    last = pca.transform(last)
    result = MatchingDegree(last, pca_test[1])
    print(result)


PCAProcess(156)

# pca = PCA(n_components = 10, svd_solver = 'randomized', whiten = True) 
# pca_points = pca.fit(rasterized_points.T)
# n2o.PointsToObj('pca_pointcloud.obj', pca_points)