"""
   list
   ****
   1) Ordered elements
   2) Hetrogeneous
   3) index starts from "0"
   4) []
   5) mutable (able to modify)
"""

# list1 = [10,20,30,40,50]
# print(list1[2],list1[-3])
# print(list1[0:2])
# print(list1[:3]) #[10,20,30]
# print(list1[2:])
# print(list1[-3:])
# print(list1[-3:-1])
# print(list1[::-1])
# print(list1[::-2])
# print(list1[::-3])


# list() - constructor
# String - Character list ['P','y','t','h','o','n']
# list1 = list("Python")
# print(list1)
# print(list1[:2]) # Py (positive index and negative index)
# print(list1[-2:])# on (positive index and negative index)
# print(list1[::-1])# reverse (nohtyP)
# print(list1[::-2]) #(nhy) (::-2)

# list1 = list([10,20,30,40,50])
# print(list1)

# len() - number of elements
# max() - highest element
# min() - smallest element
# sum() - find the sum of elements
# remove() - removes first occured element
# pop() - remove last element
# append() - add element at end of list
# extend() - add one list to another list
# insert() - add element at any index of list
# sort() - used to perform sort (ascending / decending)
# count() - find the number of repetations
# reverse() - used to reverse the list
list1 = [10,20,30,40,50]
print("Number of Elements : ",len(list1))
print("Max Element :",max(list1))
print("Min Element :",min(list1))
print("Sum of Elements :",sum(list1))

list2 = [10,20,10,20,10,30]
list2.remove(10)
print(list2)
list2.pop()
print(list2)

list3 = [10,10,20,10,20,10,30]
print(list3.count(10))
print(list3.count(20))
print(list3.count(30))

list4 = [10,50,20,40,30]
list4.sort()
print(list4)
list4.sort(reverse=True)
print(list4)

list5 = [10,50,20,40,30]
list5.reverse()
print(list5)

list6 = [10,20]
list7 = [30,40]
list6.extend(list7)
print(list6)


list8 = [10,20,30,40,50]
list8.append(60)
print(list8)

list8.insert(3,35)
print(list8)

list9 = [10,50,20,40,30]
list9.sort() #[10,20,30,40,50]
print("First Min Element :",list9[0])
print("Second Min Element :",list9[1])
print("First Max Element :",list9[-1])
print("Second Max Element :",list9[-2])