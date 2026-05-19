import matplotlib.pyplot as plt
import pandas as pd

# Example-4
x = ["Std1","Std2","Std3"]
y = [50,60,70]
bars = plt.bar(x,y,color=["red","green","blue"],width=0.5,edgecolor="orange",linewidth=2)
plt.title("Students Performance Report")
plt.xlabel("Students")
plt.ylabel("Marks")

for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),bar.get_height(),ha="center",va="bottom")
plt.show()


# Example-3
# df = pd.read_csv("chart.csv")
# x = df["age"]
# y = df["salary"]
# plt.plot(x,y,'b*--')
# plt.title("Line Plot")
# plt.xlabel("X-Axis")
# plt.ylabel("Y-Axis")
# plt.show()

# Example-2
# x = [1,2,3,4]
# y = [10,20,15,25]
# # plt.plot(x,y)
# # plt.plot(x,y,color="red",linestyle="--",marker="o") # linestyles = -, --, :   marker = o, x, *
# plt.plot(x,y,'b*--')
# plt.title("Line Plot")
# plt.xlabel("X-Axis")
# plt.ylabel("Y-Axis")
# plt.show()




# Example-1 (Line Plot)
# x = [1,2,3]
# y = [10,20,30]
# plt.plot(x,y)
# plt.show()