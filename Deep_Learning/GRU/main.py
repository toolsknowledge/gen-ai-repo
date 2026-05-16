# requirements.txt ---- tensorflow numpy pandas jupyter (3.11)

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense

# jupyter
# jupyter notebook

X = np.array([
    [1,2,3],
    [2,3,4],
    [3,4,5],
    [4,5,6]
])

y = np.array([4,5,6,7])

X = X.reshape((X.shape[0], X.shape[1], 1))

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Input

model = Sequential()

model.add(Input(shape=(3,1)))

model.add(GRU(50, activation='tanh'))

model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')

model.fit(X, y, epochs=500)

test = np.array([[5,6,7]])
test = test.reshape((1,3,1))

prediction = model.predict(test)

print(prediction)