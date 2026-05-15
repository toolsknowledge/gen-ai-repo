# def outer():
#     def inner():
#         return "Hello"
#     return inner()

# print( outer() )


# def test_func():
#     return 10,20,30,40,50

# t1 = test_func()
# e1,e2,e3,e4,e5 = t1
# print(e1,e2,e3,e4,e5)


# def test_func():
#     return [10,20,30,40,50]

# res = test_func()
# for element in res:
#     print(element)



# def division(num1,num2):
#     res = num1 / num2
#     return res

# x = division(10,5)
# print(x)



# def multiplication(num1,num2):
#     res = num1 * num2
#     print(f"Multiplication {res}")

# multiplication(200,100)
# multiplication(10,20)




# def subtraction():
#     num1 = 200
#     num2 = 100
#     res = num1 - num2
#     return res

# x = subtraction()
# print(x)

# y = subtraction()
# print(y)



# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     print(f"Addition {res}")

# addition()




# def test_func():
#     print("Welcome to functions !!!")

# test_func()
# test_func()
# test_func()
# test_func()
# test_func()

# no para - no return type
# def square():
#     num1 = 2
#     res = num1 * num1
#     print(res)

# square()

# no para - with return type
# def square():
#     num1 = 10
#     res = num1 * num1
#     return res

# res = square()
# print(res)

# with para - no return type
# def square(num1):
#     res = num1 * num1
#     print(res)

# square(100)

# with para - with return type
# def square(num1):
#     res = num1 * num1
#     return res

# res = square(1000)
# print(res)

# cube of a numbers

# keyword arguments
# def student(name,age):
#     print(name,age)

# student(age=30,name="Std1")
# student(age=40,name=None)

# Default Arguments
# def country(name="USA"):
#     print(name)

# country()
# country("India")
# country(None)

# def test_ex(num1,num2=20,num3=30):
#     print(num1,num2,num3)

# test_ex(10)
# test_ex(10,2)
# test_ex(10,2,3)

# Variable Length Arguments (*args)
# def add(*nums):
#     print(nums)
#     print(type(nums))
# add(10,20,30,40,50)
# add(100,200,300)

# def total(*prices):
#     print(sum(prices))

# total(100,200,300,400,500)

# Keyword variable Arguments (**kwargs)
# def test_ex(**data):
#     print(data,type(data))
# test_ex(name="Std1",age=20)

# def test_ex(a,b,c="Hello",*d,**e):
#     print(a,b,c,d,e)
# test_ex(10,20)
# test_ex(10,20,None,30,40,50,x=60,y=70)

# def test_ex(num1,num2):
#     return num1+num2,num1-num2,num1*num2,num1/num2
# res = test_ex(10,5)
# print(res)

# Global 
# x = 10
# def test_func():
#     # Local
#     x = 20
#     print(x)

# test_func()
# print(x)

# x = 10
# def test_func():
#     global x
#     x = 1000

# test_func()
# print(x)

# def outer():
#     def inner():
#         print("Inner")
#     inner()

# outer()

# Clousures
# def outer(num1):
#     def inner(num2):
#         return num1 + num2
#     return inner

# x = outer(10)
# res = x(5)
# print(res)

# Lambda Functions
# res = lambda x: x*x
# print(res(5))

# res = lambda num1,num2:num1 + num2
# print(res(10,5))

# students = [("Ravi",50),("Amit",80),("John",70)]
# students.sort(key=lambda x:x[1])
# print(students)

# Recursion
# def fact(n):
#     if n==1:
#         return 1
#     return n * fact(n-1)

# print(fact(5))

# 5 * fact(5-1)
# 5 * 4 * fact(4-1)
# 5 * 4 * 3 * fact(3-1)
# 5 * 4 * 3 * 2 * fact(2-1)
# 5 * 4 * 3 * 2 * 1

# def fun(n):
#     if n == 0:
#         return
#     print(n)

#     fun(n-1)
#     print(n)

# fun(3)

# First Class Function
# def test_func():
#     print("Welcome")

# x = test_func
# x()

# map() - manipulate all list elements
# we should only one parameter at a time
# nums = [1,2,3,4,5]
# res = list(map(lambda x:x*10,nums))
# print(res)

# nums = [10,20,30,40,50]
#[1,2,3,4,5]


#filter() - used to apply conditions
# we should only one parameter at a time
# nums = [1,2,3,4,5]
# res = list(filter(lambda x:x%2==0,nums))
# print(res)

# from functools import reduce
# in reduce - used to fins the sum of list
# we need to two arguments
# nums = [1,2,3,4,5]
# res = reduce(lambda num1,num2:num1+num2,nums)
# print(res)

# decorator functions, enhances "functions" functionality
# @ symbol, used to create the decorator
# def decorator(func):
#     def wrapper():
#         print("Body Gaurd 1")
#         func()
#         print("Body Gaurd 2")
#     return wrapper

# @decorator
# def hello():
#     print("MLA")

# hello()

# Generator Functions
# used to control the execution
# each statement starts with yield keyword
# next() function,used to resume the execution

# def test_func():
#     yield 100
#     yield 200
#     yield 300

# res = test_func()
# print(next(res))
# print(next(res))
# print(next(res))
# print(next(res))

# LEGB Example
# L - Local E - Enclosing G - Global B - Built-in
x = "Global"
def outer():
    # x = "enclosing"
    def inner():
        # x = "local"
        print(x)
    inner()
outer()
