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
df = pd.read_csv("employees.csv")
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