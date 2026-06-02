"""
    functions
    *********
        set of instructions called as functions
             (or)
        particular "business logic" also called as function
        
        functions are used to "reuse" business logic

        "def" is the keyword, used to declare the function

        "pass" is the keyword, used to create "empty functions"
"""
# no para - no return type
# def addition():
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         print(res)                  #300

# addition()

# no para - with return type
# def subtraction():
#     num1 = 200
#     num2 = 100
#     res = num1 - num2
#     return res

# x = subtraction()
# print(x)

# with para - no return type
# def multiply(num1,num2):
#     res = num1 * num2
#     print(res)

# multiply(200,100)

# with para - with return type
# def division(num1,num2):
#     res = num1 / num2
#     return res

# x = division(200,0)
# print(x)

# with para - with return type
# def login(uname,pwd):
#     #res = "success" if uname=="admin" and pwd=="admin@123" else "fail"
#     res=""
#     if uname=="admin" and pwd=="admin@123":
#         res = "success"
#     else:
#         res = "fail" 
    
#     return res

# res = login("admin","admin@123")
# print(res)

# default parameters
# def test_func(param1="Hello"):
#     print(param1)

# test_func()
# test_func("Welcome")
# test_func(None)

# def test_func(num1,num2=10):
#     return num1 + num2

# print(test_func(5))
# print(test_func(10,20))

# default parameters order must be last in parameters list
# def test_func(param1="Hello",param2):
#     pass
    
# in case of list, modified list will be used in next iterations
# def test_func(x=[]):   
#     x.append(1)
#     return x

# print(test_func()) # [1]
# print(test_func()) # [1,1]
#                    # [1,1,1]


# def test_func(x=None):
#     if x is None:
#         x = []
#     x.append(1)
#     return x

# print(test_func())
# print(test_func())


# by default int is immutable
# for every call num1 will be "5"
# def test_func(num1=5):
#     num1 += 1
#     return num1
# print(test_func())
# print(test_func())

# default parameters are initilized while declaraing the functions
# num1 = 100
# def test_func(param1 = num1):
#     print(param1)

# num1 = 200
# test_func()

# def test_func(sub="Gen AI",version=2):
#     print(sub,version)

# test_func(version=3,sub="Agentic AI")


# variable length arguments
# def test_func(*param1):   
#     print(param1)
#     print(type(param1))

# test_func(10,20,30,40,50)

# param1 - non default
# param2 - variable length (tuple)
# param3 - default parameter

# def test_func(param1,*param2,param3="Hello"):
#     print(param1,param2,param3)

#test_func() #TypeError: test_func() missing 1 required positional argument: 'param1'
#test_func(10) #10 () Hello
#test_func(10,20,30,40,50) #10 (20, 30, 40, 50) Hello
#test_func(10,20,param3="Welcome") #10 (20,) Welcome
#test_func(100, 10, 20, 30, 40, 50, param3="Python")


# we are able to pass only one tuple per function
# def test_func(*param1,*param2):
#     pass


# def test_func(**param1):
#     print(param1)

# test_func(name="Samba",sub="Gen AI")

# name - normal parameter
# course - default parameter
# skills - tuple
# details - dictionary
# def test_func(name,
#               course="Python",
#               *skills,
#               **details):
#     print(name)
#     print(course)
#     print(skills)
#     print(details)

# test_func("Samba","Gen AI","ML","DL","NLP",city="Hyderabad")

# normal --> default --> tuples ---> dict

# lambda - function without name
# "lambda" is the keyword, used to declare the lambda functions

# def add(num1,num2):
#     return num1 + num2
# print(add(200,100))


# add = lambda num1,num2:num1 + num2
# print(add(200,100))


# find the bigger number
# big = lambda num1,num2: num1 if num1>num2 else num2
# print(big(200,100))

# even (or) odd

# str = "Hello" len(str) --> 5

# res = lambda str:len(str)
# print(res("Python"))

"""
             map()
 [1,2,3,4,5] ---> [10,20,30,40,50]
    map() - predefined function, used to manipulate "all list elements"

                                filter()
    [100,200,300,400,500]  > 300 ---> [400,500]

    filter() - used to apply conditions on list elements
    

"""

# print(list(map(lambda param1: param1*100, [1,2,3,4,5])))

# list1 = [100,200,300,400,500]
# print(list(filter(lambda param1:param1>300,list1)))

# [1,2,3,4,5] - filter only "even" elements

# sorted() - sort the list
# names = ["Ravi","Krishna","A","Python"]
# print(sorted(names,key=lambda x:len(x)))

# sort based on marks
# students = [
#     ("Std1",85),
#     ("Std2",92),
#     ("Std3",78)
# ]

# print(sorted(students,key=lambda t1:t1[1]))

#           reduce()
# [1,2,3,4,5] -- [15]
# from functools import reduce
# print(reduce(lambda num1,num2: num1+num2, [1,2,3,4,5]))


# == (compares the "values")
# "is" checks the "memory locations"
# list1 = [10,20,30]
# #list2 = [10,20,30]
# list2 = list1
# print(list1 == list2)

# print(id(list1))
# print(id(list2))
# print(list1 is list2)

# -5 to 256 (cache) (never stores into heap area(ram)
# a = 100
# b = 100
# print(a == b)
# print(id(a))
# print(id(b))
# print(a is b)

# a = 10000
# b = 10000
# print(id(a))
# print(id(b))

# a1 = int("10000")
# b1 = int("10000")
# print(id(a1))
# print(id(b1))

# print(10 == 10)
# print("Hello" == "Hello")
# print([10] == [10])
# print(True == True)
# print(10.1 == 10.1)
# print((10) == (10))
# print({"name": "gen ai"} == {"name": "gen ai"})
# print(None == None)

# LEGB
# L - Local
# E - Enclosing
# G - Global
# B - Built-in

# num1 = 200
# def test_func():
#     #num1 = 100
#     print(num1)

# test_func()

# num1 = 100
# def test_func():
#     global num1
#     print(num1)
#     num1 = 200

# test_func()
# print(num1)

# num1 = 300
# def outer():
#     #num1 = 100

#     def inner():
#         #num1 = 200
#         print(num1)
#     inner()
# outer()


# def outer():
#     num1 = 100

#     def inner():
#         nonlocal num1
#         num1 = 200
#     inner()
#     print(num1)
# outer()















