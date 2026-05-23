# hist
import matplotlib.pyplot as plt
# marks = [35,40,42,45,50,55,58,60,62,65,68,70,72,75,78,80,82,85,88,90,92,95]
# plt.figure(figsize=(10,6))
# bins = 5
# 95 - 35 = 60 / 5 = 12
# 35 - 47 (Bin1) 4
# 47 - 59 (Bin2) 3
# 59 - 71 (Bin3) 5
# 71 - 83 (Bin4) 5
# 83 - 95 (Bin5) 5
# plt.hist(marks,bins=5,color='red',edgecolor='black',alpha=0.2)
# plt.title("Marks Distribution",fontsize=16)
# plt.xlabel("Marks",fontsize=12)
# plt.ylabel("Students",fontsize=12)
# plt.grid(True)
# plt.show()

subjects = ['Math','Science','English']
marks = [85,90,78]
attendance = [90,85,95]

plt.figure(figsize=(12,8))

plt.subplot(2,2,1)
plt.plot(subjects,marks,'ro--')
plt.title("Marks Trend")

plt.subplot(2,2,2)
plt.bar(subjects,marks,color='skyblue')
plt.title("Bar Graph")

plt.subplot(2,2,3)
plt.pie(marks,labels=subjects,autopct='%1.1f%%')
plt.title("Pie")

plt.subplot(2,2,4)
plt.hist(marks,bins=2,color='yellow',edgecolor='black',alpha=0.5)
plt.title("Histo")

plt.show()







