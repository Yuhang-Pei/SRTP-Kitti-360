import numpy as np
import os
import pickle
from math import sin, cos

# ------------------------------------------------------------------------------------------

# Object Saving and Loading Functions
# Can deal with any kind of object

'''
    @brief: Save a python object into a .pkl file
    @param obj: the object to save
    @param file_name: the name of the file to save the object
'''
def save_obj(obj, file_name):
    with open(file_name + '.pkl', 'wb') as file:
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)


'''
    @brief: Load the data of an object from the .pkl file
    @param file_name: the name of the file containing object data
'''
def load_obj(file_name):
    with open(file_name + '.pkl', 'rb') as file:
        return pickle.load(file)

# ------------------------------------------------------------------------------------------

# Type Conversion Functions
# Change file type of pointcloud file (including .npz, .txt and .obj)

'''
	@brief: Transform points array to .obj file
	@param obj_file_name: The given name of .obj file
	@param points: The array of points, where each point is 3-dimensional
'''
def PointsToObj(obj_file_name, points):
    with open(file = obj_file_name, mode = 'w') as obj:
        output = '# ' + repr(len(points)) + '\n'
        obj.write(output)
        for i in range(len(points)):
            output = 'v ' + repr(points[i][0]) + ' ' + repr(points[i][1]) + ' ' + repr(points[i][2]) + '\n'
            obj.write(output)


'''
	@brief: Transform .npz file to .obj file
	@param obj_file_name: The given name of .obj file
	@param npz_file_name: .npz file extracted from ShapeNet, containing 3-dimensional coordinates of all the points
'''
def NpzToObj(obj_file_name, npz_file_name, if_std: bool):
	data = np.load(npz_file_name)
	points = data['points']
	if if_std == False:
		PointsToObj(obj_file_name, points)
	else:
		PointsToObj(obj_file_name, Standardize(points))


'''
	@brief: Transform .npz file to .txt file
	@param txt_file_name: The given name of .txt file
	@param npz_file_name: .npz file extracted from ShapeNet
'''
def NpzToTxt(txt_file_name, npz_file_name):
	data = np.load(npz_file_name)
	points = data['points']
	with open(file = txt_file_name, mode = 'w') as txt:
		for i in range(len(points)):
			output = repr(points[i][0]) + ' ' + repr(points[i][1]) + ' ' + repr(points[i][2]) + '\n'
			txt.write(output)

'''
	@brief: Transform .txt file to .obj file
	@param obj_file_name: The given name of .txt file
	@param txt_file_name: .txt file extracted from KITTI-360
'''
def TxtToObj(obj_file_name, txt_file_name):
	with open(obj_file_name, 'w') as obj_file:
		with open(txt_file_name, 'r') as txt_file:
			for line in txt_file:
				obj_file.write('v ' + line)


'''
	@brief: Batch conversion from .npz file to .obj file
	@param root_path: The root path, under with all 'pointcloud.npz' will be converted to 'points.obj'
'''
def BatchConversion(root_path, file_type):
	dirlist = os.listdir(root_path)
	if file_type == 'obj':
		for d in dirlist:
			sub_dir = os.path.join(root_path, d)
			sub_dirlist = os.listdir(sub_dir)
			for f in sub_dirlist:
				if f == 'pointcloud.npz':
					NpzToObj(os.path.join(sub_dir, 'points.obj'), os.path.join(sub_dir, f), True)
	elif file_type == 'txt':
		for d in dirlist:
			sub_dir = os.path.join(root_path, d)
			sub_dirlist = os.listdir(sub_dir)
			for f in sub_dirlist:
				if f == 'pointcloud.npz':
					NpzToTxt(os.path.join(sub_dir, 'points.txt'), os.path.join(sub_dir, f))
					print(os.path.join(sub_dir, 'points.txt'))

# ------------------------------------------------------------------------------------------

# Processing Functions of Point Cloud

'''
    @brief: Standardize the points by translaton and scaling
            so as to centralize the point cloud and fit the standard size of models
    @param points: List of points
'''
def Standardize(points):
	std_points = np.array(points)
	x_min = min(std_points[:, 0])
	x_max = max(std_points[:, 0])
	y_min = min(std_points[:, 1])
	y_max = max(std_points[:, 1])
	z_min = min(std_points[:, 2])
	z_max = max(std_points[:, 2])

	std_points[:, 0] -= (x_max + x_min) / 2
	std_points[:, 1] -= (y_max + y_min) / 2
	std_points[:, 2] -= (z_max + z_min) / 2

	ax = 1.2 / (x_max - x_min)
	ay = 1.2 / (y_max - y_min)
	az = 1.2 / (z_max - z_min)
	a = min(ax, ay, az)
	std_points *= a

	return std_points


'''
	@brief: Rotate the point cloud extracted from KITTI-360, so that its direction is 
			same as the direction of models in ShapeNet
	@param points: List of points
'''
def Rotate(points, rotate_vector):
	x = rotate_vector[0]
	y = rotate_vector[1]
	z = -rotate_vector[2]
	Rx = np.array([[1, 0, 0], [0, cos(x), sin(x)], [0, -sin(x), cos(x)]])
	Ry = np.array([[cos(y), 0, -sin(y)], [0, 1, 0], [sin(y), 0, cos(y)]])
	Rz = np.array([[cos(z), sin(z), 0], [-sin(z), cos(z), 0], [0, 0, 1]])
	R = np.matmul(np.matmul(Rx, Ry), Rz)
	rotated_points = np.matmul(points, R)

	rotate_matrix = np.array([[0, 0, -1], [-1, 0, 0], [0, 1, 0]])
	return np.matmul(rotated_points, rotate_matrix)


# ------------------------------------------------------------------------------------------

# Testing and Debugging Functions

'''
	@brief: Add Gaussian noise to the original point cloud
	@param origin_points: The original point cloud
	@param mean: The average value of Gaussian distribution
'''
def GaussianNoise(origin_points, mean):
	noise = np.random.normal(0, mean, origin_points.shape)
	new_points = origin_points + noise
	return new_points

# ------------------------------------------------------------------------------------------

def main():
	#BatchConversion('E:\\SRTP\\part\\', 'obj')
	NpzToObj('E:\\SRTP\\part\\000\\points.obj', 'E:\\SRTP\\part\\000\\pointcloud.npz', True)

if __name__ == '__main__':
	main()