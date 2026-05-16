import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

data = {
    "Outlook": ["Sunny","Sunny","Overcast","Rain","Rain","Rain","Overcast","Sunny"],   
    "Temperature":["Hot","Hot","Hot","Mild","Cool","Cool","Mild","Hot"],
    "Humidity":["High","High","High","High","Normal","Normal","Normal","High"],
    "Play":["No","No","Yes","Yes","Yes","No","Yes","No"]
}

df = pd.DataFrame(data)

le = LabelEncoder()

for column in df.columns:
    df[column] = le.fit_transform(df[column])

X = df.drop("Play",axis=1)

y = df["Play"]


model = DecisionTreeClassifier(criterion="entropy")
model.fit(X,y)

res = model.predict([[0,0,0]])
print(res[0])


