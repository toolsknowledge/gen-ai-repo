"""
    ordered
    mutable
    allows duplicates
    allows hetrogeneous
    []
    index starts from "0"

    list stores references, not actual values/objects
"""

# list1 = [10,10.1,True,"Hello",20,30,40,50]
# print(list1[3],list1[-5])       #Hello Hello
# print(list1[1:3])
# print(list1[:2])
# print(list1[2:])
# print(list1[::-1])
# x = list1[:] # complete copy
# list1[0] = 1000
# print(x)

# append() - add one element
# extens() - adds multiple elements
# insert() - add element at particular index
# remove() - delete first occured element Ex.remove(10)
# pop() - removes last element
# clear() - removes all elements
# sort() - sort the list elements
# reverse() - reverse list elements
# len()
# max()
# min()

# list1 = [10,20]
# list1.append(30)
# print(list1)

# list1.extend([40,50])
# print(list1)

# list1.insert(2,25)
# print(list1)

# list1.extend([10,20,30])
# print(list1)

# list1.remove(10)
# print(list1)

# list1.pop()
# print(list1)

# list1.clear()
# print(list1)

# list1 = [10,50,20,40,30]
# list1.sort() #[10, 20, 30, 40, 50] ascending
# print(list1)

# list1.sort(reverse=True) # decending
# print(list1) # [50, 40, 30, 20, 10]

# list1 = [10,20,30,40,50]
# list1.reverse()
# print(list1)

# list1 = [10,20,30,40,50]
# print(len(list1))
# print(max(list1))
# print(min(list1))
# print(sum(list1))
# print(sum(list1) / len(list1))

# shallow copy
# "copy()" and ":" meant for "shallow copy"
# list1 = [10,20,30]
# list2 = list1.copy()
# list2 = list1[:]
# list2.append(40)
# print(list1)
# print(list2)

# deep copy
# list1 = [10,20,30]
# list2 = list1
# list1.append(40)
# print(list1)
# print(list2)

# list1 = [[10,20],[30,40],[50,60],[70,80],[90,100]]
# for inner_list in list1:
#     for element in inner_list:
#         print(element, end=" ")

# list1 = [10,20,30]
# list2 = list((10,20,30))
# list3 = list("Hello")
# print(list1)
# print(list2)
# print(list3)

# list1 = [x for x in range(5)]
# print(list1)

# list1 = [x for x in range(10) if x%2 == 0]
# print(list1)

