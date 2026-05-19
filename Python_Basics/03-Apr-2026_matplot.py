# matplotlib --> graphs, charts
# matplotlib --> numpy & pandas

# pie Chart
# import matplotlib.pyplot as plt
# stds = ["Std1","Std2","Std3"]
# marks = [40,30,30]
# plt.pie(marks,labels=stds,autopct='%1.1f%%')
# plt.show()



# Subplot
# import matplotlib.pyplot as plt
# plt.subplot(1,3,1)
# plt.plot([1,2,3],[1,4,9])

# plt.subplot(1,3,2)
# plt.bar([1,2,3],[3,2,5])

# plt.subplot(1,3,3)
# plt.hist([1,2,2,3,3,3,4,4,5], bins=5)

# plt.show()





# Histogram (Frequency)
# import matplotlib.pyplot as plt
# data = [1,2,2,3,3,3,4,4,5]
# plt.hist(data, bins=5)
# plt.show()
# 1 - 1. 2 - 2.  3 - 3. 4 - 2. 5 - 1
# bins - 5 min = 1. max = 5. range = 5 - 1 = 4 --> 5bins = 4(range)/5(bins) = 0.8
# 1 - 1.8 - 1
# 1.8 - 2.6 - 2
# 2.6 - 3.4 - 3
# 3.4 - 4.2 - 2
# 4.2 - 5 - 1




# Scatter Plot
# import matplotlib.pyplot as plt
# x = [1,2,3,4]
# y = [10,20,25,30]
# plt.scatter(x,y)
# plt.show()




# Bar Chart (Example-1)
# import matplotlib.pyplot as plt
# x = ["Std1","Std2","Std3","Std4","Std5"]
# y = [60,70,80,90,100]
# plt.bar(x,y)
# plt.barh(x,y)
# plt.xlabel("Names")
# plt.ylabel("Marks")
# plt.title("Students Vs Marks")
# plt.show()

# Bar Chart (Example-2)
# import matplotlib.pyplot as plt
# import pandas as pd
# df = pd.read_csv("Book1.csv")
# x = df["Name"]
# y = df["Salary"]
# bars = plt.bar(x,y,color=["red","green","blue"],width=0.5,edgecolor="yellow")
# plt.xlabel("Emp Names")
# plt.ylabel("Salary")
# plt.title("Emp Names Vs Salary")

# for bar in bars:
#     plt.text(bar.get_x()+bar.get_width()/2, bar.get_height(),bar.get_height(), ha="center", va="bottom")

# plt.show()








# Line Plot
# import matplotlib.pyplot as plt
# import pandas as pd
# df = pd.read_csv("Book1.csv")
# x = df["Age"]
# y = df["Salary"]
# x = [1,2,3,4,5]
# y = [10,20,30,40,50]
# plt.plot(x,y) 
# plt.plot(x, y, color='red')
# plt.plot(x,y,color='green',linestyle='--')
# plt.plot(x,y,color="blue",linestyle='--', marker='o')
# plt.plot(x,y,color="blue",linestyle='--', marker='X')
# plt.title("Line Plot")
# plt.xlabel("Days")
# plt.ylabel("Sales")
# plt.show()

