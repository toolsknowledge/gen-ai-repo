# collection of variables and functions called as class
# "class" is the keyword, used to declare the class
# __init__, used to declare the constructor
# constructor,used to initilize the instance variables
# instance members are availble in separate copies for each object


# class Test:
#     # no para - no return type
#     def add1(self):
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         print(res)

#     # no para - with return type
#     def add2(self):
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         return res
    
#     # with para - no return type
#     def add3(self,param1,param2):
#         res = param1 + param2
#         print(res)
    
#     # with para - with return type
#     def add4(self,param1,param2):
#         res = param1 + param2
#         return res

# obj1 = Test()
# obj1.add1()

# x = obj1.add2()
# print(x)

# obj1.add3(200,100)

# y = obj1.add4(200,100)
# print(y)

# class Test:
#     def __init__(self,param1,param2):
#         self.num1 = param1
#         self.num2 = param2

# obj1 = Test(200,100)
# x = obj1.num1
# y = obj1.num2
# res = x + y
# print(res)


# class Test:
#     def __init__(self):
#         self.num1 = 200

# obj1 = Test()
# obj1.num1 = 2000

# obj2 = Test()
# x = obj2.num1
# print(x)


# class Test:
#     def __init__(self):
#         self.num1 = 200
#         self.num2 = 100

# obj1 = Test()
# x = obj1.num1
# y = obj1.num2
# res = x + y
# print(res)

# inheritance
# getting the data from parent class to child class called as inheritance

# single level inheritance
# class Parent:
#     def __init__(self):
#         self.num1 = 200

# class Child(Parent):
#     def __init__(self):
#         super().__init__()
#         self.num2 = 100

# obj = Child()
# x = obj.num1
# y = obj.num2
# res = x + y
# print(res)

# single level inheritance
# class Parent:
#     def __init__(self,num1):
#         self.num1 = num1
# class Child(Parent):
#     def __init__(self, num1,num2):
#         super().__init__(num1)
#         self.num2 = num2

# obj = Child(200,100)
# x = obj.num1
# y = obj.num2
# res = x + y
# print(res)


# multilevel inheritance
# class Parent:
#     def test1(self):
#         print("Parent !!!")
# class Child(Parent):
#     def test2(self):
#         print("Child !!!")
# class Subchild(Child):
#     def test3(self):
#         print("Subchild !!!")

# obj = Subchild()
# obj.test1()
# obj.test2()
# obj.test3()

# multilevel inheritance
# class Parent:
#     def test1(self):
#         print("Hello")

# class Child(Parent):
#     def test2(self):
#         super().test1()

# class Subchild(Child):
#     def test3(self):
#         super().test2()

# obj = Subchild()
# obj.test3()

# multiple inheritance
# class Parent1:
#     def test1(self):
#         print("Parent1")

# class Parent2:
#     def test2(self):
#         print("Parent2")

# class Child(Parent1,Parent2):
#     pass

# obj = Child()
# obj.test1()
# obj.test2()

# hirarichal
# class Parent:
#     def test1(self):
#         print("Parent !!!")
# class Child1(Parent):
#     def test2(self):
#         print("Child1 !!!")
# class Child2(Parent):
#     def test2(self):
#         print("Child2 !!!")

# obj1 = Child1()
# obj1.test1()
# obj1.test2()

# obj2 = Child2()
# obj2.test1()
# obj2.test2()

# hybrid (multiple + hirarichal)
# class Parent:
#     def test1(self):
#         print("Parent !!!")
# class Child1(Parent):
#     def test2(self):
#         print("Child1 !!!")
# class Child2(Parent):
#     def test3(self):
#         print("Child2 !!!")
# class Subchild(Child1,Child2):
#     def test4(self):
#         print("Subchild !!!")
# obj = Subchild()
# obj.test1()
# obj.test2()
# obj.test3()
# obj.test4()

# overriding
# class Parent:
#     def db_conn(self):
#         print("oracle conn soon...!")

# class Child(Parent):
#     def db_conn(self):
#         print("mongodb conn soon...!")

# obj = Child()
# obj.db_conn()

# class level variable
# class Test:
#     cmp = "Infosys !!!"

#     def __init__(self):
#         pass

# obj1 = Test()
# obj2 = Test()
# print(Test.cmp)
# print(obj1.cmp)
# print(obj2.cmp)

# Test.cmp = "Accenture !!!"
# print(Test.cmp)

# class Test:
#     name = "Hello"

#     @classmethod
#     def change_name(cls):
#         cls.name = "Welcome"

# print(Test.name)
# Test.change_name()
# print(Test.name)

# Encapsulation
# class Bank:
#     def __init__(self,balance):
#         self.__balance = balance
#     def deposit(self,amount):
#         self.__balance += amount
#         print(self.__balance)
#     def withdraw(self,amount):
#         self.__balance -= amount
#         print(self.__balance)

# bank = Bank(5000)
# bank.deposit(5000)
# bank.withdraw(5000)


# from abc import ABC, abstractmethod
# class Test1(ABC):
#     @abstractmethod
#     def m1(self):
#         pass
# class Test2(Test1):
#     def m1(self):
#         print("Hello")

# obj = Test2()
# obj.m1()

# class Demo:
#     def __str__(self):
#         return "Dunder Methods !!!"

# obj = Demo()
# print(obj)


# add = lambda num1,num2 : num1 + num2
# print(add(20,10))

# bigger = lambda num1,num2 : num1 if num1>num2 else num2
# print(bigger(200,100))

# res = lambda num1 : "even" if num1%2 == 0 else "odd"
# print(res(10))
# print(res(9))

# res = lambda num1 : num1%2==0
# print(res(10))
# print(res(9))


# res = tuple(map(lambda num1: num1*num1, [10,20,30,40,50]))
# print(res)

nums = [1,2,3,4,5]
# print(list(filter(lambda num1: num1%2 == 0, nums)))
# from functools import reduce
# print(reduce(lambda num1,num2:num1+num2,nums))