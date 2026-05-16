import pandas as pd
df = pd.read_excel("sales.xlsx")
df["Total"] = df["Quantity"] * df["Price"]
daily_sales = df.groupby("Date")["Total"].sum()
best_product = df.groupby("Product")["Quantity"].sum().idxmin()
monthly_rev = df["Total"].sum()
print(df)
print(monthly_rev)







# import pandas as pd
# df = pd.read_excel("attendance.xlsx")
# df["Attendance%"] = (df["Present"] / df["Total_Classes"]) * 100
# low_attendance = df[df["Attendance%"]<75]
# print(low_attendance)




# import pandas as pd
# df = pd.read_excel("transactions.xlsx")


# credits = df[df["Type"] == "Credit"]["Amount"].sum()


# debits = df[df["Type"] == "Debit"]["Amount"].sum()

# balance = credits - debits

# highest_expenses = df[df["Type"] == "Debit"].groupby("Category").sum().idxmin()

# print(credits)
# print(debits)
# print(balance)
# print(highest_expenses)