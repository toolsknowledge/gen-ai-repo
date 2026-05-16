import pandas as pd

data = {
    "name" : ["Emp1","Emp2","Emp3"],
    "age" : [22,24,26],
    "salary" : [10000,20000,30000]
}
# df = pd.DataFrame(data) # iloc --> row index
# print( df.iloc[0] )   # row 0
# print( df.iloc[1] )   # row 1
# print( df.iloc[2] )   # row 2

# print(df.iloc[2,2])   # row2 & col2
# print(df.iloc[1,1])   # row1 & col1

# print( df.iloc[0:2] ) # 0row -- includes & 2row excludes

# print(df.iloc[:,0])   #all rows & col0 
# print(df.iloc[:,2])   #all rows & col2

# print(df.loc[0])

# print( df )
# print( df.loc[1,"salary"] )
# print( df.loc[2,"age"] )

# print( df.loc[:,["name","salary"]] )
# print( df.loc[ df["age"]>23 ] )
# iloc() --> row index, unable to apply conditions
# loc() --> col index, apply conditions

# df = pd.DataFrame(data)
# # print(df.reset_index())
# # print(df.reset_index(drop=True))
# df.index = ["A","B","C"]
# print(df)




# df = pd.read_csv("employees_null.csv")

# Example1
# print(df)
# print("--------------------------------")

# Example2
# print(df.isnull()) # missed value represent with True
# print("--------------------------------")

# Example3
# print(df.notnull()) # opp to isnull()
# print("--------------------------------")

# Example4
# print(df.isnull().sum()) # col wise report
# print("--------------------------------")


# Example5
# drop_any_row = df.dropna() # if row contains null, it will drop
# print(drop_any_row)


# Example6
# df_drop_all = df.dropna(how='all') # if entire row contains null, it will drop
# print(df_drop_all)

# Example7
#drop_row_based_age = df.dropna(subset=["age"]) #drop row, when age is null
#print(drop_row_based_age)

# Example8
# drop_row_based_salary = df.dropna(subset=["salary"]) #drop row, when salary is null
# print(drop_row_based_salary)

# Example9
# drop_row_based_age_salary = df.dropna(subset=["age","salary"]) # drop row when "age and salary" are null
# print(drop_row_based_age_salary)


# Example10
# fill_with_zero = df.fillna(0) # fill missed values with 0
# print(fill_with_zero)

# Example11
# df["age"] = df["age"].fillna(df["age"].mean())                  #fill empty with mean (age)
# df["salary"] = df["salary"].fillna(df["salary"].mean())         #fill empty with mean (salary)
# print(df)

# Example12
# print(df)
# print("-----------------------------")
# forward_fill = df.ffill()
# print(forward_fill)
# backward_fill = df.bfill()
# print(backward_fill)
# print("-----------------------------")










# df = pd.read_csv("employees.csv")
# Add the column & modify the column
# df["salary"] = [10000,20000]
# df["age"] = df["age"] + 2
# df["salary"] = 100000
# print(df)

# print( df.drop("age", axis=1) ) # delete age col # axis=1 representing col

# print( df.drop(0, axis=0) )     #delete row 0, axis=0 representing row