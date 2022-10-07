import numpy as np
from sklearn.decomposition import PCA
from utility import save_obj

'''
    @brief: Read the rasterized PCA matrix of training data from .dat file
    @param pca_matrix: this matrix is used to store the data reading from the file
'''
def ReadPCAMatrixData(pca_matrix: list):
    with open(file = 'pca_matrix.dat', mode = 'r') as pca_matrix_file:
        for line in pca_matrix_file:
            line = [ord(x) - ord('0') for x in line]
            line.pop()
            pca_matrix.append(line)


'''
    @brief: PCA process contains 3 steps:
            create the object,
            fit with training data
            save pca into .pkl file
    @param pca_train: rasterized training data
'''
def PCATrainProcess(pca_train_data: list):
    # create PCA object
    pca = PCA(n_components = len(pca_train_data))

    #fit with training data
    pca_train_data = np.array(pca_train_data)
    pca_train_result = pca.fit_transform(pca_train_data)

    # save pca object and training data after PCA transformation
    save_obj(pca, 'pca')
    save_obj(pca_train_result, 'pca_train_result')


def main():
    pca_train_data = list()
    ReadPCAMatrixData(pca_train_data)

    print('size of training data: ', len(pca_train_data))
    print('dimension: ', len(pca_train_data[0]))

    PCATrainProcess(pca_train_data)


if __name__ == '__main__':
    main()