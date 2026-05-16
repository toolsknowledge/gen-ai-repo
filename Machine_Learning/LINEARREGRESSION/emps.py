import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression 
from sklearn.model_selection import train_test_split
# Features (input)
X = np.array([1,2,3,4,5,6]).reshape(-1,1)
#label (output)
y = np.array([3,5,7,9,11,13])
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.33,random_state=42)

model = LinearRegression()
model.fit(X_train,y_train)

y_pred = model.predict(X_test)
print("Actula Salary :",y_test)
print("Predicted Salary :",y_pred)

new_sal = model.predict([[7]])
#plt.scatter(X,y,color="blue")
#plt.plot(X,y,color="red")
#plt.show()
# plt.plot(X,y,color="red")
# plt.show()
plt.show()




