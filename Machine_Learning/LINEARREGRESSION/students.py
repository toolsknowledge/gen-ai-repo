import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

X = np.array([1,2,3,4,5]).reshape(-1,1)
# [[1],[2],[3],[4],[5]]

y = np.array([20,40,60,80,100])

model = LinearRegression()

model.fit(X,y)

marks = model.predict([[10]])
print(marks[0])


