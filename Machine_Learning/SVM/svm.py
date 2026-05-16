from sklearn import svm
X = [[1],[2],[4],[5]]
y = [0,0,1,1]
model = svm.SVC(kernel="linear")
model.fit(X,y)
print(model.coef_) #w
print(model.intercept_) #b
# wx + b
print( model.predict([[10]]) )