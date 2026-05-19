# tensorflow - Deep Learning Library (engine)
import tensorflow as tf

# keras - used to build deep learning "models" (steering)
from tensorflow import keras

# numpy used to work with lists
import numpy as np

# import FastAPI
from fastapi import FastAPI

# import BaseModel
# BaseModel used to define Schema (define clear datatypes / format)
from pydantic import BaseModel


class Test(BaseModel):
    num : float


# input
X = np.array([[1],[2],[3],[4]])

# output
y = np.array([[1],[4],[9],[16]])    # y = x * x

# create model
model = keras.Sequential([
    keras.layers.Dense(3,activation='relu'),
    keras.layers.Dense(1)
])

# compile
model.compile(
    optimizer='adam',
    loss='mean_squared_error'
)

# Train the model
model.fit(X,y,epochs=500)

app = FastAPI()

class InputData(BaseModel):
    value:float

@app.get("/")
def home():
    return {"message" : "welcome to FastAPI !!!"}

@app.post("/predict")
def predict(obj:Test):
    res = model.predict(np.array([[obj.num]]))
    # [[11.3]] "11.3" float("11.3") -- 11.3
    return {"result" : float(res[0][0])}




