# append() - add element at end of list
# insert() - add element at particular index
# extend() - add one list to the another list
# remove() - used to remove element from list
# pop() - used to remove "last element"
# pop(index) / del - used to delete particular element based on index
# clear() - used to delete all list elements
# index() - know the index of a first occured element
# count() - know the occurance of list element
# len() - used to know list elements
# sort() - used to sort the list elements in ascending order (mutable)
# sort(reverse=True) - used to sort the list elements in decending order (mutable)
# sorted() - used to sort the list elements (immutable)
# reverse() - used to reverse the list elements
# max() - used to find the max element in a list
# min() - used to find the min element in list
# sum() - used to find the sum of list elements



# list1 = [[1, 2, 3],
#          [4, 5, 6],
#          [7, 8, 9]]
# print(list1[0][0]) #1
# print(list1[2][2]) #9

# for row in list1:
#     for value in row:
#         print(value,end="\n")



# list1 = [1,2,[3,4],5]
# x = list1[2]
# print(x[0],x[1])




# list1 = [10,20,30,40,50]
# print(len(list1))
# print(max(list1))
# print(min(list1))
# print(sum(list1))




# list1 = [1,2,3,4,5]
# new_list = [num for num in list1 if num%2 != 0]
# print(new_list)



# list1 = [1,2,3,4,5]
# new_list = [i*i for i in list1]
# print(new_list)
# print(list1)



# list1 = [10,20,30,40,50]
# for element in list1:
#     print(element)

# for element in range(len(list1)):
#     print(list1[element])


# list1 = [10,30,20]
# list1.sort()
# list1.reverse()
# print(list1)


# list1 = [10,30,20]
# list1.reverse()
# print(list1)



#list1 = [5,2,8,1]
#list1.sort() # ascending
#print(list1)
#list1.sort(reverse=True) # decending order
#print(list1)

# new_list = sorted(list1)
# print(new_list)
# print(list1)



# list1 = [10,20,30,40,50,20]
# print(list1.index(20))
# print(list1.count(20))
# print(len(list1))




# list1 = [10,20,30,40,50,20]
# list1.remove(20)   # remove 20. (first occured element)
# print(list1)
# list1.pop()        # remove last element
# print(list1)
# list1.pop(1)       # remove element at particular index
# print(list1)
# del list1[0]       # remove element at particular index
# print(list1)
# list1.clear()      # clear all elements
# print(list1)



# list1 = [1,2]
# list1.append(3)
# print(list1)
# list1.insert(1,100)
# print(list1)
# list1.extend([4,5])
# print(list1)


# list1 = [10,20,30,40,50]
# list1[0] = 1000
# print(list1)


# list1 = [10,20,30,40,50]
# print(list1[0], list1[-5])
# print(list1[2], list1[-3])


# list1 = [10,20,30]
# print(list1)
# list2 = [10,"Hello",True,3.14]
# print(list2)
# list3 = list((10,20,30))
# print(list3)
# list4 = [1] * 5
# print(list4)
