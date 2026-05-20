# Function - Business logic called as Function
# Reuse the Business logic
# "def" is the keyword, used to define the Function
# "pass" is the keyword, representing empty function


# First Class Functions
# store "functions" in "variables"
# pass as "argument"
# return from "functions"

# def test_func():
#     print("Hello")

# x = test_func
# x()

def test_func1():
    print("Hello")

def test_func2(func):
    func()

test_func2(test_func1)


# reduce()
# reduce() function, used to find the sum of list elements
# from functools import reduce
# nums = [1,2,3,4,5]
# res = reduce(lambda num1,num2:num1+num2,nums)
# print(res)



# filter()
# apply conditions on list elements
# nums = [1,2,3,4,5,6]
# res = list(filter(lambda x:x%2==0,nums))
# print(res)


# map()
# manipulate all elements in list
# nums = [1,2,3,4,5]          #[100,200,300,400,500]
# res = list(map(lambda x:x*100,nums))
# print(res)


# Decorator Example
# def decorator(func):
#     def wrapper():
#         print("Secuirity 1")
#         func()
#         print("Security 2")
#     return wrapper

# @decorator
# def hello():
#     print("MLA")

# hello()

# LEGB Rule L-Local,E-Enclosing,G-Global,B-Built-In
# x = "global"
# def outer():
#     # x = "enclosing"
#     def inner():
#         # x = "local"
#         print(x)
#     inner()
# outer()



# students = [("Std3",50),("Std2",40),("Std1",60)]
# students.sort(key=lambda x:x[0])
# print(students)


# addition = lambda num1,num2:num1+num2
# print(addition(200,100))

# sqaure = lambda x:x*x
# print(sqaure(10))


# Closure
# def outer(num1):
#     def inner(num2):
#         return num1+num2
#     return inner
# x = outer(200)
# res = x(100)
# print(res)


# Function Definition
# def test_func():
#     print("Hello")

# x = test_func
# print(x)
# x()


# Nested Function
# def outer():
#     def inner():
#         print("Hello")
#     inner()
# outer()

# global variable
# x = 100
# def test_func():
#     # local variable
#     x = 200
#     print(x) # accessing local variable

# test_func()
# print(x) # accessing global variable




# def test_func(num1,num2):
#     return num1+num2, num1-num2,num1*num2,num1/num2

# res = test_func(200,100)
# print(type(res))



# param1 & param2 - positional parameters
# param3 - variable length parameter
# param4 - keyword variable arguments
# def test_func(param1,param2,*param3,**param4):
#     print(param1,param2,param3,param4)

# test_func(10,20,30,40,name="Samba",age=40)


# keyword variable arguments
# def test_func(**data):
#     print(data,type(data))

# test_func(name="Samba",age=40)


# Variable Length Arguments
# def test_func(*nums): #nums - ()
#     print(nums, sum(nums),type(nums), list(nums))

# test_func(10,20,30,40,50)
# test_func(100,200,300)


# Default arguments
# def test_func(name="Samba"):
#     print(name)

# test_func()
# test_func(name="Gen AI")
# test_func(name=None)


# keyword arguments
# def test_func(name,age):
#     print(name,age)

# test_func(age=40,name="Samba")
# test_func(age=30,name=None)
# test_func("Samba",40)




# write the code for square of a number


# Example-5 (with parameters - with return type)
# def addition(num1,num2):
#     res = num1 + num2
#     return res

# x = addition(200,100)
# print(x)


# Example-4 (with para - no return type)
# def addition(num1,num2):
#     res = num1 + num2
#     print(res)

# addition(200,100)


# Example-3 (no para & with return type)
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     return res
# x = addition()
# print(x)



# Example-2 (no para - no return type)
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     print(res)

# addition()


# Example-1
# def func_one():
#     print("welcome to functions !!!") 

# func_one()
# func_one()
# func_one()