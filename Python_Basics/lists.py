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


# list1 = list("Python")
# print(list1)            # ['P', 'y', 't', 'h', 'o', 'n']
# Py (+) (-)
# on (+) (-)
# Reverse (::-1) / reverse()

# filter() - apply conditions
# map() - manipulate every element
# reduce() - sum of list elements

# from functools import reduce
# evens = filter(lambda num1:num1%2==0,[1,2,3,4,5]) # [2,4]
# squares = map(lambda num1:num1*num1,evens) # [4,16]
# res = reduce(lambda num1,num2:num1+num2,squares) # 20
# print(res)

# remove duplicates
# nums = [1,2,1,2,"Hello","hello"]
# res = list(set(nums))
# print(res)

# count() - 1--> 2. 2 --> 2
# print(nums.count(1))
# print(nums.count(2))
# print(nums.count("Hello"))

nums = [1,2,3,2,4,5,1]
# [1,2]
# display only duplicates
# print(list(set([x for x in nums if nums.count(x)>1])))
# [1, 2, 2, 1] {1, 2}


# nums = [1,2,3,2,4,5,1,5]
# list1 = []
# for x in nums :
#     if nums.count(x)>1:
#       list1.append(x)
#       print(set(list1))


# nums = [10,40,5,70] # [5,10,40,70] sort() 1st 2nd last 2nd last
# max
# find the 2nd max element
# min
# 2nd min element
# nums.sort()
# print("Max Element : ",nums[-1])
# print("2nd Max Element :",nums[-2])
# print("Min Element :",nums[0])
# print("2nd Min Element :",nums[1])

# list1 = [10,20]
# list2 = [30,40]

# list1.extend(list2)
# print(list1) # [10,20,30,40]

# list1.append(list2)
# print(list1) # [10,20,[30,40]]

# list1 = [10]
# print(list1 * 3)

# list2 = [10,20,30]
# print(list2 * 2)

# list3 = [[]]
# print(list3 * 3)

# shallow copy
# copy() function
# list1 = [[1,2],[3,4]]
# list2 = list1.copy()
# list1[0][0] = 100
# print(list2)

# deepcopy
# import copy
# from copy import deepcopy
# list1 = [[1,2],[3,4]]
# list2 = deepcopy(list1)
# list1[0][0] = 100
# print(list2)

