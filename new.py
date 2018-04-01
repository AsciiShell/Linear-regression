import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
print("r-squared:", r_value ** 2)
plt.plot(x, y, 'o', label='original data')
plt.plot(x, intercept + slope * x, 'r', label='fitted line')
plt.legend()
plt.show()
pass
