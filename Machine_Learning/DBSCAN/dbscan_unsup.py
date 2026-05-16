import numpy as np
#Density Based Spatial Clustering Application with Noise
#Divide datapoints into number of clusters based on attributes
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
# Step 1: Dataset
X = np.array([[1,1],
              [1,2],
              [2,1],
              [8,8],
              [8,9],
              [50,50]])

# Step 2: Apply DBSCAN
model = DBSCAN(eps=2, min_samples=3)
labels = model.fit_predict(X)
print("Cluster Labels:", labels)
# Step 3: Scatter Plot
plt.scatter(X[:,0], X[:,1], c=labels)
# Step 4: Labels & Title
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("DBSCAN Clustering")
# Step 5: Show Plot
plt.show()