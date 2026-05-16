import numpy as np
from sklearn.decomposition import PCA
X = np.array([[4,11],
              [8,4],
              [13,5],
              [7,14]])
model = PCA(n_components=1)
X_new = model.fit_transform(X)
print(X_new)