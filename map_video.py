from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style

def short_proj():
    return np.dot(axes3d.Axes3D.get_proj(ax1), scale)

style.use('ggplot')
np.set_printoptions(threshold=np.inf)
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

x = [[20, 20], [-20, -20]]
z = [[20, -20], [20, -20]]
y = [[0, 0], [0, 0]]
ax1.plot_wireframe(x,y,z, color = "green", linewidth = 1.0, linestyle = "-")
y = [[100, 100], [100, 100]]
ax1.plot_wireframe(x,y,z, color = "green", linewidth = 1.0, linestyle = "-")

x_scale = 1.0
z_scale = 2.0
y_scale = 7.8125

scale = np.diag([x_scale, y_scale, z_scale, 1.0])
scale = scale * (1.0 / scale.max())
scale[3,3] = 1.0

ax1.get_proj = short_proj

ax1.set_xlabel('x axis')
ax1.set_ylabel('z axis')
ax1.set_zlabel('y axis')

plt.xlim(0, 128)
plt.xticks([0, 128])
ax1.set_zlim(0, 256)
ax1.set_zticks([0, 256])
ax1.set_ylim(0, 80)
my_y_ticks = np.linspace(0, 80, 5, endpoint = True)
ax1.set_yticks(my_y_ticks)
ax1.set_ymargin(0.1)
plt.show()
#plt.savefig("test.jpg")
