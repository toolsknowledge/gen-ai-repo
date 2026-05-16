from sklearn.naive_bayes import GaussianNB
# read data from excel sheet
X = [[2],[5],[6],[1]]
y = ["Fail","Pass","Pass","Fail"]
model = GaussianNB()
model.fit(X,y)

# read inpuit from swagger
res = model.predict([[4]])

# send result
print(res)

