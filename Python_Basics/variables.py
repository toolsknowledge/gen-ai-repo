# print("Hello,welcome to python !!!")

# from rich import print
# print("[red]Hello,welcome to python[/red]")
# print("[bold green]Hello[/bold green]")

# Falsy - 0, 0.0, "",[],(),{},set(),None,False
# print(bool(0),end=" ")
# print(bool({}))

# Truth
# 1, -100, 10.1, "Hello",[1,2],(10,20),{"name":"Samba"}
# print(bool(-100))

# list1 = [10,20,30,40,50]
# tuple1 = (10,20,30,40,50)

# import sys
# print(sys.getsizeof(list1))
# print(sys.getsizeof(tuple1))


# == (compares the values)
# "is" checking memory locations

# list1 = [10,20,30,40,50]
# list2 = [10,20,30,40,50]
# print(list1 == list2) # True
# print(list1 is list2) # False

# list1 = [10,20,30,40,50]
# list2 = list1
# print(list1 == list2)
# print(list1 is list2)

# x = 100
# y = 100
# print(x == y)
# print(x is y) # False. (True) # -5 to 256

# x1 = int("257")
# y1 = int("257")
# print(x1 is y1)