import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

data = {
    "hours" : [1,2,3,4,5,6],
    "pass" : [0,0,0,1,1,1]
}

df = pd.DataFrame(data)
X = df[["hours"]]
y = df["pass"]

model = LogisticRegression() # sigmoid
model.fit(X,y)

res = model.predict([[10]])
prob = model.predict_proba([[3]])

plt.scatter(df["hours"],df["pass"])
plt.title("Student Graph !!!")
plt.xlabel("Hours")
plt.ylabel("Pass")
plt.show()