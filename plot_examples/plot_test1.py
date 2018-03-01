import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x = np.array([2,5,6,8,9,12,45,67,89,2345,23,45,566])
#print(x,"\n", x[:2], "\n", x[:5])

np.random.seed(2000)
y = np.random.standard_normal((20, 2)).cumsum(axis=0)



y[:, 0] = y[:, 0] * 100

print(y)

plt.figure(figsize=(9,4))
plt.subplot(121)
plt.plot(y[:, 0], lw=1.5, label='1st')
plt.plot(y[:, 0], 'ro')
plt.legend(loc=0)
plt.xlabel('index')
plt.ylabel('value')
plt.title('First Data Set')
plt.grid(True)
plt.axis('tight')

plt.subplot(122)
plt.bar(np.arange(len(y)), y[:, 1], width=0.5, color='g', label='2nd')
plt.grid(True)
plt.legend(loc=0)
plt.axis('tight')
plt.xlabel('index')
plt.title('2nd Data Set')

plt.show()
