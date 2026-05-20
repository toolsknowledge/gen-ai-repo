import matplotlib.pyplot as plt
import pandas as pd

# Example-1 (Line Plot)
# x = [1,2,3]
# y = [10,20,30]
# plt.plot(x,y)
# plt.show()

# Example-2 (Line Plot)
# x = [1,2,3,4]
# y = [10,20,15,25]
# # plt.plot(x,y)
# # plt.plot(x,y,color="red",linestyle=":",marker="o") # linestyles:-,--,: marker=o,x,*
# plt.plot(x,y,'g*--')
# plt.title("Line Chart")
# plt.xlabel("X-Axis")
# plt.ylabel("Y-Axis")
# plt.show()


# Example-3 (Line Plot with pandas)
# df = pd.read_csv("chart.csv")
# x = df["age"]
# y = df["salary"]
# plt.plot(x,y,'g*--')
# plt.title("Age & Salary")
# plt.xlabel("Age")
# plt.ylabel("Salary")
# plt.show()

# Example-4 (Bar Chart)
# x = ['A','B','C']
# y = [10,20,15]
# # plt.bar(x,y)
# bars = plt.bar(x,y,color=['red','green'],width=0.5,edgecolor='yellow')
# plt.title("Bar Title")
# plt.xlabel("X-Axis")
# plt.ylabel("Y-Axis")

# for bar in bars:
#     plt.text(bar.get_x() + bar.get_width()/2,bar.get_height(),bar.get_height(),ha="center",va="bottom")

# plt.show()

# Pie Chart
# subjects = ['Math','Science','English','Python','Java']
# marks = [95,88,76,98,85]

# colors = ['gold','skyblue','lightgreen','orange','pink']
# explode = (0,0,0,0.1,0)

# plt.figure(figsize=(8,8))

# plt.pie(marks,
#         labels=subjects,
#         colors=colors,
#         explode=explode,
#         autopct='%1.3f%%',
#         shadow=True,
#         startangle=90)
# plt.title("Student Marks Distribution")
# plt.legend(title="Subjects")
# plt.show()

# Scatter plot
study_hours = [1,2,3,4,5,6,7,8]
marks = [35,40,50,60,65,70,85,95]
sizes = [100,120,140,160,180,200,220,240]
colors = ['red','blue','green','orange','purple','brown','pink','cyan']
plt.figure(figsize=(10,6))
plt.scatter(study_hours,marks,s=sizes,c=colors,alpha=0.7,edgecolors='black',marker='o')
plt.title("Study Hours vs Marks Analysis",fontsize=16)
plt.xlabel("Study Hours",fontsize=12)
plt.ylabel("Marks",fontsize=12)
plt.annotate('Top Student',xy=(8,95),xytext=(8,80),arrowprops=dict(facecolor='red',shrink=0.10))
plt.grid(True)
plt.show()




