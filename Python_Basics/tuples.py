"""
    tuple
    *****
        ordered elements
        hetrogeneous
        immutable
        ()
        fast in retrival operation
        best memory utilization
"""

# t1 = (10)
# print(type(t1)) #<class 'int'>

# t2 = (10,)
# print(type(t2)) #<class 'tuple'>

# t1 = (10,20,30,40,50)
# print(t1[0],t1[-5])
# display 10,20 (pos & neg)
# display 40,50 (pos & neg)
# reverse

# t1 = 10,20,30,40,50,10,20,10
# print(len(t1))
# print(max(t1))
# print(min(t1))
# print(sum(t1))
# print(t1.count(10))
# print(t1.count(20))
# print(t1.index(30))


# num1 = 10
# num2 = 20
# num2,num1 = num1,num2
# print(num1)

# t1 = 10,20,30,40,50
# for element in t1:
#     print(element)

# t1 = tuple([10,20,30])
# print(t1)


# t1 = ((10,20),(30,40),(50,60),(70,80),(90,100))
# for inner_tuple in t1:
#     for element in inner_tuple:
#         print(element,end=" ")

# t1 = (10,20,30,40,50)
# t1[0] = 1000

# t1 = ([10,20],[30,40])
# t1[0][0] = 1000
# print(t1)

# t1 = (10,20)
# t2 = (30,40)
# t3 = t1 + t2
# print(t3)

# t4 = t3 * 2
# print(t4)

# print(t4.count(10))
# print(10 in t4)
# print(10 not in t4)

# import sys
# list1 = [10,20,30,40,50]
# tuple1 = (10,20,30,40,50)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(tuple1))

# d1 = {
#     (1,2) : "Hello"
# }
# print(d1)


# list1 = [10,20,30,40,50]
# t1 = tuple(list1)
# print(t1)

# t1 = (100,200,300,400,500)
# list1 = list(t1)
# print(list1)
