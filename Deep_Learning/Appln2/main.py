import numpy as np
import pandas as pd
# split data --> 1) Train. 2) Test
from sklearn.model_selection import train_test_split
# Normalization
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
import matplotlib.pyplot as plt
# load predefined DataSet
from sklearn.datasets import load_breast_cancer

data = load_breast_cancer()
# Input (X)
X = data.data
# output
y = data.target

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


model = keras.Sequential([
    keras.layers.Dense(32,activation='relu'),
    keras.layers.Dense(16,activation='relu'),
    keras.layers.Dense(1,activation='sigmoid')
])


model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

history = model.fit(X_train,y_train,epochs=100,validation_data=(X_test,y_test))

# history.history["accuracy"] --> Train (80%). plot
# history.history["val_accuracy"] ---> Test (20%) plot


if model.predict(X_test[0].reshape(1,-1))[0][0] > 0.5:
    print("Safe")
else:
    print("Danger")


plt.plot(history.history["accuracy"])
plt.plot(history.history["val_accuracy"])
plt.xlabel("EPochs")
plt.ylabel("Accuracy")
plt.title("Train <> Test")
plt.legend(["Train","Test"])
plt.show()





