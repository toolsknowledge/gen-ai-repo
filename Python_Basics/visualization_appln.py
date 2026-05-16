import matplotlib.pyplot as plt

# 1 - row. 2 - number of columns in rows  3 = order
plt.subplot(1,3,1)
plt.plot([1,2,3],[4,5,6])
plt.title("Graph 1")

plt.subplot(1,3,2)
plt.bar([1,2,3],[4,5,6])
plt.title("Graph2")

plt.subplot(1,3,3)
plt.plot([1,2,3],[4,5,6])
plt.title("Graph 3")

plt.show()


# x = [1,2,3,4,5]
# y1 = [10,20,30,40,50]
# y2 = [5,15,25,35,45]
# y3 = [15,25,35,45,55]
# plt.plot(x,y1,label="Line1")
# plt.plot(x,y2,label="Line2")
# plt.plot(x,y3,label="Line3")
# plt.legend()
# plt.show()



# x = [1,2,3,4,5]
# y = [10,15,13,17,20]
# plt.scatter(x,y)
# plt.title("Scatter Plot")
# plt.show()


# marks = [45,60,70,80,90,55,67,73,88,92]
# plt.hist(marks, bins=5)
# plt.show()


# categories = ["Food","Rent","Travel","Others"]
# amount = [5000,10000,2000,3000]
# plt.pie(amount,labels=categories,autopct='%1.1f%%')
# plt.show()


# subjects = ["Math","Science","English","Physics","Chemistry","Gen AI"]
# marks = [50,60,80,70,99,50]
# plt.pie(marks,labels=subjects,autopct='%1.3f%%')
# plt.title("Marks Distribution")
# plt.show()



# subjects = ["Math","Science","English","Physics","Chemistry","Gen AI"]
# marks = [50,60,80,70,99,50]
# plt.barh(subjects,marks)
# plt.show()


# employees jira 
# excel sheet (server)
# read this sheet rest api
# pandas
# pyplot



# subjects = ["Math","Science","English","Physics","Chemistry","Gen AI"]
# marks = [50,60,80,70,99,50]
# plt.bar(subjects,marks)
# plt.title("Students Progress")
# plt.xlabel("Subjects")
# plt.ylabel("Marks")
# plt.show()


# subjects = ["Math","Science","English","Physics","Chemistry","Gen AI"]
# marks = [50,60,80,70,99,50]
# plt.plot(subjects,marks,marker='o')
# plt.title("Students Marks")
# plt.xlabel("Subjects")
# plt.ylabel("Marks")
# plt.show()



# x = [1,2,3,4,5]
# y = [10,20,15,25,30]
# plt.plot(x,y)
# plt.title("Simple Line Graph")
# plt.xlabel("X Values")
# plt.ylabel("Y Values")
# plt.show()
