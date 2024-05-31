import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys

#read data from file
data = np.genfromtxt('results.txt', delimiter=',')
print(data)

#split data into x,y,z
x = data[:,0]
y = data[:,1]
z = data[:,2]

#plot surface using x,y,z
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(x, y, z)

#set labels and title
ax.set_title('3D Plot')
ax.set_xlabel('itens per bucket')
ax.set_ylabel('number of buckets')
ax.set_zlabel('time consumption (s)')
plt.show()

