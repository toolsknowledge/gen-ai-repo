import pandas as pd

# Example-1
# print(pd.__version__)

# Example-2
# nums = [10,20,30,40,50]
# res = pd.Series(nums)
# print(res)

# Example-3
# data = ["Python","ML","DL","NLP","GenAI","AgenticAI"]
# res = pd.Series(data,index=["a","b","c","d","e","f"])
# print(res)

# Example-4
# marks = [80,90,95]
# res = pd.Series(marks,index=["Std1","Std2","Std3"])
# print(res)
# print(res["Std3"])

# Example-5
# employees = {
#     "EmpId": [101,102,103],
#     "Department":["IT","HR","Finance"],
#     "Salary":[60000,45000,70000]
# }
# df = pd.DataFrame(employees,index=["a","b","c"])
# print(df)

# Example-6
# df = pd.read_csv("employees.csv")
# print(df)
# print(df.head()) # read 5 rows
# print(df.head(3)) # read 3 rows
# print(df.head(10)) # read 10 rows

# print(df.tail()) # read last 5 rows
# print(df.tail(10)) # read last 10 rows

# print(df.shape) # displays rows and cols

# print(df.columns) # displays all the col names

# print(df.info()) # displaying - col name, datatype, null values

# print(df["Salary"].describe()) # mathematical calculations
# print(df[["Salary","Bonus"]].describe()) # mathematical calculations

# print(df["Name"]) # display single column
# print(df[["Name","Age"]].head()) # display more than one col
# print(df[df["Salary"]>70000]) # display employees whose salary > 70000
# print(df[df["Department"] == "IT"]) # displays only IT Department
# print(df.groupby("Department")["Salary"].mean()) # find mean salary department wise 

# print(df.sort_values("Salary",ascending=False).head(1)[["Name","Department","Designation"]]) #  display highest paid employee
# print(df[(df["Salary"]>70000) & (df["Department"]=="IT")]) # apply multiple conditions

df = pd.read_csv("employees_null.csv")
print(df)
# nulls replaced with True
# print(df.isnull())

# nulls replaced with False
# print(df.notnull())

# nulls age column
# print(df["age"].isnull())

# nulls in salary column
# print(df["salary"].isnull())

# nulls in column wise
# print(df.isnull().sum())

# column wise nulls percentage 
# print( df.isnull().sum() / len(df) * 100 )

# replace missed values with 0
# print(df.fillna(0))

# implement forward fill
# print(df.ffill())

# implement the backward fill
# print(df.bfill())

# fill missed age with average age
# df["age"] = df["age"].fillna(df["age"].mean())

# fill missed salary with average salary
# df["salary"] = df["salary"].fillna(df["salary"].mean())
# print(df)

# handle multiple missed values 
# df.fillna({
#     "age":df["age"].mean(),
#     "salary":df["salary"].mean()
# },inplace=True)
# print(df)

print("---------------------")
# if any column missed then delete entire row
# print(df.dropna())

# if all columns are null, then only delete the row
# print(df.dropna(how="all"))

# if age & salary are null, then only drop the row
# print(df.dropna(subset=["age","salary"]))

# if row contains two non nulls,it wont delete
# print(df.dropna(thresh=2))