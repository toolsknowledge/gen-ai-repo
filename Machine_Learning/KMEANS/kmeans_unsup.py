import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
X = np.array([[1,2],[2,3],[3,4],[8,8],[9,9],[10,10]]);
model = KMeans(n_clusters=2)
model.fit(X)
labels = model.labels_
plt.scatter(X[:,0],X[:,1],c=labels)
plt.show()
print(labels)