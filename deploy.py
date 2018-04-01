import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from sklearn.datasets import load_boston

boston = load_boston()
dataset = pd.DataFrame(boston.data, columns=boston.feature_names)
dataset['target'] = boston.target
observations = len(dataset)
variables = dataset.columns[:-1]
X = dataset.ix[:, :-1]
y = dataset['target'].values
Xc = sm.add_constant(X)
linear_regression = sm.OLS(y, Xc)
fitted_model = linear_regression.fit()
a = fitted_model.summary()
print(a)
plt.plot(y, Xc, 'o', label='original data')
# plt.plot(Xc, intercept + slope * x, 'r', label='fitted line')
plt.legend()
plt.show()
