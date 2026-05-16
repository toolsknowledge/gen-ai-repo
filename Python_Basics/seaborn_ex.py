import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# df = sns.load_dataset("tips")
# print(df.head())
# sns.lineplot(x="day",y="total_bill",data=df)
# plt.show()

print(sns.get_dataset_names())


# data = pd.DataFrame({
#     "Month":["Jan","Feb","Mar","April"],
#     "Marks":[70,75,80,90]
# })
# sns.lineplot(x="Month",y="Marks",data=data)

# data = pd.DataFrame({
#     "Subject":["Sub1","Sub2","Sub3","Sub4","Sub5"],
#     "Marks":[80,85,90,95,90]
# })
# sns.barplot(x="Subject",y="Marks",data=data)

# data = pd.DataFrame({
#     "Hours":[1,2,3,4,5],
#     "Marks":[50,60,70,80,90]
# })
# sns.scatterplot(x="Hours",y="Marks",data=data)

# data = np.random.randint(40,100,100)
# sns.histplot(data,bins=5)

# data = pd.DataFrame({
#     "Math":[80,90,70],
#     "Science":[85,88,72],
#     "English":[75,92,68]
# })
# sns.heatmap(data,annot=True,cmap="YlGnBu")

# data = pd.DataFrame({
#     "Class":["A","A","A","B","B","B"],
#     "Marks":[70,80,90,60,80,85]
# })
# sns.boxplot(x="Class",y="Marks",data=data)

# plt.show()