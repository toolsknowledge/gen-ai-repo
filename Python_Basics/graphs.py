import matplotlib.pyplot as plt

# Line Graph
# Bar Chart
# Horizontal Bar
# Pie
# Histogram
# Scatter
# Subplot


plt.subplot(2,2,1)
x = ["Std1","Std2","Std3","Std4","Std5"]
y = [90,80,70,60,50]
plt.plot(x,
         y,
         marker='o',
         markersize=10,
         markerfacecolor="red",
         markeredgecolor="green")
plt.title("Simple Line Graph")
plt.xlabel("Students")
plt.ylabel("Marks")


plt.subplot(2,2,2)
x = ["Std1","Std2","Std3","Std4","Std5"]
y = [90,80,70,60,50]
plt.bar(x,y)
plt.title("Students Bar Chart")
plt.xlabel("Students")
plt.ylabel("Marks")

plt.subplot(2,2,3)
x = ["Std1","Std2","Std3","Std4","Std5"]
y = [90,80,70,60,50]
plt.barh(x,y)
plt.title("Students Bar Chart")
plt.xlabel("Students")
plt.ylabel("Marks")


plt.subplot(2,2,4)
x = [5,10,15,20,25]
y = [10,15,20,25,30]
plt.scatter(x,y)
plt.title("Scatter Plot")
plt.xlabel("X Values")
plt.ylabel("Y Values")
plt.grid()

plt.show()


# x = [5,10,15,20,25]
# y1 = [15,25,35,45,55]
# plt.plot(x,y1,color="red",label="Line1")
# y2 = [25,35,45,55,65]
# plt.plot(x,y2,color="blue",label="Line2")
# plt.legend()
# plt.show()


# marks = [45,60,70,80,90,55,67,73,88,92]
# plt.hist(marks,bins=5,color="green",edgecolor="black")
# plt.title("Marks Range")
# plt.grid()
# plt.show()


# subjects = ["English","Maths","Science","Social","Physics","Chemistry"]
# marks = [60,70,80,90,60,70]
# plt.pie(marks,labels=subjects,autopct="%1.1f%%")
# plt.title("Marks Distribution")
# plt.show()


# x = ["Std1","Std2","Std3","Std4","Std5"]
# y = [90,80,70,60,50]
# plt.barh(x,y)
# plt.title("Students Bar Chart")
# plt.xlabel("Students")
# plt.ylabel("Marks")
# plt.show()



# x = ["Std1","Std2","Std3","Std4","Std5"]
# y = [90,80,70,60,50]
# plt.bar(x,y)
# plt.title("Students Bar Chart")
# plt.xlabel("Students")
# plt.ylabel("Marks")
# plt.show()




# #LINE CHART 
# #X
# #Y
# x = ["Std1","Std2","Std3","Std4","Std5"]
# y = [90,80,70,60,50]
# plt.plot(x,
#          y,
#          marker='o',
#          markersize=10,
#          markerfacecolor="red",
#          markeredgecolor="green")
# plt.title("Simple Line Graph")
# plt.xlabel("Students")
# plt.ylabel("Marks")
# plt.show()
