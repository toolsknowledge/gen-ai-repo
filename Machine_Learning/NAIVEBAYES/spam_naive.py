from sklearn.naive_bayes import MultinomialNB
X = [[2,1],[1,3],[2,0],[0,2]]
y = ["Spam","Spam","NotSpam","NotSpam"]
model = MultinomialNB()
model.fit(X,y)
print(model.predict([[2,3]]))


