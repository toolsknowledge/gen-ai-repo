from sklearn.neighbors import KNeighborsClassifier
X = [[150,50],[160,60],[170,70],[180,80],[185,90]]
y = ["Slim","Slim","Fat","Fat","Fat"]
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X,y)
res = model.predict([[165,65]])
print(res[0])

