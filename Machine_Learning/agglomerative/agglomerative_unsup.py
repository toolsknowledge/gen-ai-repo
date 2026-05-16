from sklearn.cluster import AgglomerativeClustering
import numpy as np
X = np.array([[1,2],[2,3],[8,8],[9,9],[15,2],[16,3],[20,1],[22,2],[50,1]])
model = AgglomerativeClustering(n_clusters=4)
labels = model.fit_predict(X)
print(labels)