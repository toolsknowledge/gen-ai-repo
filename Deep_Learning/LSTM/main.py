# Import libraries
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator

# Dataset
data = np.array([10,20,30,40,50,60,70,80,90,100])

# Reshape data
data = data.reshape(-1,1)

# Create sequence
n_input = 3

generator = TimeseriesGenerator(
    data,
    data,
    length=n_input,
    batch_size=1
)

# Create model
model = Sequential()

# Add LSTM Layer
model.add(
    LSTM(
        50,
        activation='relu',
        input_shape=(n_input,1)
    )
)

# Add output layer
model.add(Dense(1))

# Compile model
model.compile(
    optimizer='adam',
    loss='mse'
)

# Train model
model.fit(
    generator,
    epochs=200
)

# Prediction input
x_input = np.array([80,90,100])

# Reshape input
x_input = x_input.reshape((1,n_input,1))

# Predict
prediction = model.predict(x_input)

print(prediction)