"""
   tuple
   *****
    1) Ordered
    2) Immutable
    3) allows duplicates
    4) ()
    5) Faster Compared to Lists
    6) Best Memory Utilization compared to Lists
    7) Hetrogeneous Elements
    8) Hashtable
"""
# t1 = (10,20,30,40,50)
# print(t1[2],t1[-3])
# # slicing
# # reverse
# print(type(t1))



# t1 = (10)
# print(type(t1))
# t2 = (10,)
# print(type(t2))

# t1 = (10,20,30,40,50)
# print(len(t1))
# print(max(t1))
# print(min(t1))
# print(sum(t1))
# print(t1.count(10))
# print(t1.index(40))
# t2 = (10,50,20,40,30)
# print(sorted(t2))

# t1 = (10,20,30,40,50)
# t1[0] = 1000  #TypeError: 'tuple' object does not support item assignment

# t1 = (10,20,30,40,50)
# list1 = list(t1)
# list1[0] = 1000
# t2 = tuple(list1)
# print(t2)

# import sys
# list1 = [10,20,30,40,50]
# tuple1 = (10,20,30,40,50)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(tuple1))

# unpacking
# t1 = (10,20,30,40,50)
# e1,e2,e3,e4,e5 = t1
# print(type(e1))
# print(e1,e2,e3,e4,e5)

# x1,*x2,x3 = t1
# print(x2) #[20, 30, 40]
# a1,a2,*a3 = x2
# print(a3)
# a4 = a3
# print(a4)

# t1 = (100,200,"Hello",True,10.1,None)
# e1,e2,*e3 = t1
# print(e3)
# *e4,x = e3
# print(e4)

# #packing
# t1 = 10,20,30
# print(t1)
# print(type(t1))
# #unpacking
# x,y,z = t1
# print(x,y,z)

# x,y,z = 10,20,30
# print(x,y,z)

# num1 = 100
# num2 = 200
# num2,num1 = num1,num2
# print(num1,num2)

# t1 = ([10],[20],[30])
# t1[0].append(100)
# print(t1)

# t1 = 10,20,30,40,50
# for element in t1:
#     print(element)

# t1 = ((10,20),(30,40),(50,60))
# for inner_tuple in t1:
#     for element in inner_tuple:
#         print(element,end=" ")

# t1 = (1,2)
# t2 = (3,4)
# t3 = t1 + t2
# print(t3)

# t4 = t3 * 2
# print(t4)

# print(2 in t4)
# print(200 in t4)
# print(2 not in t4)
# print(200 not in t4)

# d1 = {
#     (1,2):"Hello"
# }
# print(d1)
# d2 = {
#     [1,2] : "Hello"
# }
# print(d2)

print( hash((1,2,3)) )
print( hash([1,2,3] ))