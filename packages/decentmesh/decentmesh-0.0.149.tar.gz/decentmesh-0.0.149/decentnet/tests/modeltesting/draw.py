import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator

a = np.loadtxt("points.txt", delimiter=",")
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

surf = ax.scatter(a[:, 4], a[:, 0], a[:, 5], c=a[:, 5], cmap=cm.coolwarm)

# Customize the z axis.
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

figure, axis = plt.subplots(2, 2)

# For Sine Function
axis[0, 0].plot(a[:, 0], a[:, 5])
axis[0, 0].set_title("Take Profit")

# For Cosine Function
axis[0, 1].plot(a[:, 1], a[:, 5])
axis[0, 1].set_title("Stop loss")

# For Tangent Function
axis[1, 0].plot(a[:, 2], a[:, 5])
axis[1, 0].set_title("Trail arm")

# For Tanh Function
axis[1, 1].plot(a[:, 4], a[:, 5])
axis[1, 1].set_title("Trail buy")

# Combine all.yaml the operations and display
plt.show()
