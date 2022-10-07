# with open('train.txt', 'r') as file1:
#     with open('test.txt', 'r') as file2:
#         for i in range(100000):
#             line1 = file1.readline()
#             line2 = file2.readline()
#             if line1 != line2:
#                 print('False')

# with open('tmp.txt', 'r') as file1:
#     line = file1.readline()
#     with open('train.txt', 'w') as file2:
#         for i in range(len(line)):
#             if line[i] == '1':
#                 file2.write(repr(i) + '\n')
from math import sin
print(sin(-0.4343581680770375))