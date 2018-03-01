import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

y = np.random.standard_normal((1000, 2))
c = np.random.randint(0, 10, len(y))
print(y)


plt.figure(figsize=(7,5))
plt.hist(y, label=['1st', '2nd'], color=['b', 'g'], stacked=True, bins=20)
plt.grid(True)
plt.legend(loc=0)
plt.xlabel('value')
plt.ylabel('frequency')
plt.title('Histogram')


plt.show()
