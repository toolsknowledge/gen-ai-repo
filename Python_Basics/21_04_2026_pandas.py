import pandas as pd

# Example-1 (1D)
# data = [10,20,30,40,50]
# dataFrame = pd.Series(data)
# print(dataFrame)

# Example-2 (2D)
data = {
    "name" :["Std1","Std2","Std3","Std4","Std5","Std6","Std7","Std8","Std9","Std10","Std1","Std12"],
    "marks" :[10,20,30,40,50,60,70,80,90,100,110,120]
}
df = pd.DataFrame(data)
print(df)

# print(df.head()) # 5rows
# print(df.head(7)) # 7 rows

# print(df.tail()) # last 5rows
# print(df.tail(8)) # last 8rows

# print(df.sample()) # one random row
# print(df.sample(5)) # five random rows

# print(df.sample(frac=0.5)) # 50% of random data

# print(df.shape)   #rows,cols
# print(df.size)    #no of elements
# print(df.ndim)    #2
# print(df.columns) #column names
# print(df.index)   #index range
# print(df.dtypes)  #datatypes of columns

# print( df.info() )
# print( df.describe() )  # first numerical col (mathematical calculations)
# print( df.describe(include="all") ) # include all numerical columns

# print(df.iloc[0])   # row at "0" position
# print(df.loc[0])    # based on label

# df.index = [100,200,300,400,500,600,700,800,900,1000,1100,1200]
# print(df)
# print(df.loc[600])
# print(df.iloc[5])

# print(df.loc[0:2])          #0 and 2 includes
# print(df.iloc[0:2])         #0 will include and 2 will exclude

# print(df[ df['marks']>50 ])
# print(df[df['marks'] == 50])
# print(df[(df["marks"]>50) & (df["marks"]<90)])

# print(df.sort_values("marks"))
# print(df.sort_values("marks",ascending=False))
# print(df.sort_index())

# df = pd.read_csv("employees_null.csv")
# print(df["name"])
# print(df[["name","age"]])
# print( df.isnull() )   
# print( df.notnull() )
# print(df.dropna())
# print(df.dropna(axis=1))
# print(df.fillna(0))
# print(df.fillna(10))
# print(df.ffill())
# print(df.bfill())
# print(df["age"].fillna(df["age"].mean()))


# df = pd.read_csv("emps.csv")
# read single col
# print(df["name"])

# read multiple colums
# print(df[["name","age"]])

# read cell value
# print(df.loc[0,"name"])

# add the new col
# df["bonus"] = df["salary"] * 0.10
# print(df)

# delete col
# df.drop("bonus",axis=1,inplace=True)


# df1 = pd.read_csv("emps.csv")
# df2 = pd.read_csv("department.csv")
# # merge two csv files
# merged_df = pd.merge(df1,df2)
# print(merged_df)

# print( merged_df.groupby("department")["salary"].mean() )
# print( merged_df.groupby("department")["salary"].max() )
# print( merged_df.groupby("department")["salary"].min() )
# print( merged_df.groupby("department")["salary"].sum() )

# df1 = pd.read_csv("emps.csv")
# df2 = pd.read_csv("department.csv")
# merged_df = pd.merge(df1,df2) # inner join
# print( merged_df.sort_values(by='salary') )     # ascending
# print( merged_df.sort_values(by='salary',ascending=False) ) # decending
# print( merged_df[merged_df["salary"]>45000] )

# df = pd.read_csv("students.csv")

#check missing values
#print(df.isnull())

#count of missing values (col wise)
#print(df.isnull().sum())

# df.dropna(inplace=True)
# print(df)

# df["marks"] =  df["marks"].fillna(0,inplace=True) 
# print(df)

# df["marks"] = df["marks"].ffill()
# print(df)

# df["marks"] = df["marks"].bfill()
# print(df)

# print( df.replace("Hyderabad","HYD") )
# print(df)