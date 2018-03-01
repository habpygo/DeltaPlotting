import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

y = np.random.standard_normal((1000, 2))
c = np.random.randint(0, 10, len(y))
print(y)
"""
plt.figure(figsize=(7,5))
plt.plot(y[:, 0], y[:, 1], 'ro')
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')
"""

plt.figure(figsize=(7,5))
plt.scatter(y[:, 0], y[:, 1], c=c,  marker='o')
plt.colorbar()
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')


plt.show()
