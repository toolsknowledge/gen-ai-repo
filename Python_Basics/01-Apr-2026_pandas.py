# pandas
# built on top of numpy
# data manipulation & analysis
# tabular data
# pip install pandas
# pip install openpyxl


import pandas as pd


# x = pd.Series([10,20,30,40,50]) #ID
# print(x)

# y = pd.DataFrame({
#     "name":["Std1","Std2"],           #2D
#     "age":[20,22]
# })
# print(y)


df = pd.read_csv("Book1.csv")
#df = pd.read_csv("Book1.csv",index_col=0,header=None)
#print(df.head()) #head() - 5rows
#print(df.tail()) #tail() - last 5 rows
#print(df.info()) #info() -- give datatype (metadata)
#print(df.describe()) #describe() -- gives count,std,max,min,.....
#print(df.shape) #(10,3) (10 rows and 3 cols)
#print(df.columns) #display only cols
#print(df.dtypes) #knows the datatypes

#print(df["Name"])
#print(df[["Name","Age"]])

# print(df)
# print("-------------------------------")
# print(df.iloc[0]) # by index
# print("------------------------------")
# print(df.loc[0]) # by label

# print(df[df["Age"]>30])
