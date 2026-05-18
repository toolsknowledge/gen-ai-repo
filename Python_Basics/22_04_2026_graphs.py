import matplotlib.pyplot as plt
import pandas as pd

# Plot Graph
# x = [1,2,3,4]
# y = [10,20,15,25]
# df = pd.read_csv("graphs.csv")
# x = df["x"]
# y = df["y"]
# # plt.plot(x,y)
# # plt.plot(x,y,color='red')
# plt.plot(x,y,color='orange',linestyle=':',marker='x') # linestyles = "-", "--", ":"  marker = "o","x", "*"
# plt.xlabel("X Axis")
# plt.ylabel("Y Axis")
# plt.title("Line Plot")
# plt.show()

# Bar Graph
# x = ["std1","std2","std3","std4","std5"]
# y = [60,70,80,90,100]
# bars = plt.bar(x,y,color=['red','green','blue'],width=0.5,edgecolor='black')
# for bar in bars:
#     plt.text(-0.25 + bar.get_x() + bar.get_width()/2, bar.get_height(), bar.get_height(), ha="center",va="center")

# #plt.barh(x,y)
# plt.title("Bar Chart")
# plt.xlabel("Students")
# plt.ylabel("Marks")
# plt.show()


# Pie Chart
# subjects = ['Math','Science','English','Computer']
# marks = [80,90,70,95]
# colors=['gold','lightblue','lightgreen','orange']
# explode = [0,0.2,0,0.1]
# plt.pie(marks,
#         labels=subjects,
#         colors=colors,
#         autopct='%1.5f%%',
#         explode=explode,
#         shadow=True,
#         textprops={'fontsize':10},
#         wedgeprops={'edgecolor':'red','linewidth':2},
#         startangle=90)
# plt.title("Students Marks Distribution")
# plt.xlabel("Subjects")
# plt.ylabel("Marks")
# plt.show()

# Histogram

# marks = [45, 50, 55, 60, 62, 65, 67, 70, 72, 75,
#          78, 80, 82, 85, 88, 90, 92, 95, 97, 100]

# max = 100
# min = 45
# diff = 55
# bins = 55 / 5 = 11
# bin1 = 45 - 56 = 3 (45 included, 56 excluded)
# bin2 = 56 - 67 = 4 (56 included - 67 excluded)
# last bin - both are included 

# plt.figure(figsize=(8,6))

# plt.hist(marks,
#          bins=5,
#          color='skyblue',
#          edgecolor='black')

# plt.title("Students Marks Distribution")
# plt.xlabel("Marks")
# plt.ylabel("Freqency")
# plt.show()

# Scatter
# hours = [1,2,3,4,5,6]
# marks = [35,45,50,60,70,85]
# plt.figure(figsize=(8,6))
# plt.scatter(hours,
#             marks,
#             s=200,
#             color='red',
#             marker='o',
#             edgecolors='yellow',
#             alpha=0.7)
# plt.grid(True)
# plt.show()

# import matplotlib.pyplot as plt
# months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
# sales = [100, 150, 200, 180, 250]
# plt.fill_between(months, sales)
# plt.title("Monthly Sales Area Graph")
# plt.xlabel("Months")
# plt.ylabel("Sales")
# plt.show()


# plt.figure(figsize=(10,8))
# plt.subplot(2,2,1)
# x = [1,2,3,4]
# y = [10,20,30,40]
# plt.plot(x,y)

# plt.subplot(2,2,2)
# plt.bar(x,y)

# plt.subplot(2,2,3)
# marks = [45, 50, 55, 60, 62, 65, 67, 70, 72, 75,
#          78, 80, 82, 85, 88, 90, 92, 95, 97, 100]
# plt.hist(marks,
#          bins=5,
#          color='skyblue',
#          edgecolor='black')

# plt.title("Students Marks Distribution")
# plt.xlabel("Marks")
# plt.ylabel("Freqency")

# plt.show()




