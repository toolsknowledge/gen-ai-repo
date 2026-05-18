# OOPS - Object Oriented Programming System
# class - collection of variables and functions
# class is the keyword, used to declare the class

# Example-1
# class Test:
#     def wish(self):             # self - current object (Ex this in java)
#         print('welcome to oops !!!')

# t1 = Test()     #creating the object
# t1.wish()       #welcome to oops !!!

# Example-2
# class Test:
#     # no para - no return 
#     def add1(self):
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         print(f'Addition : {res}')

#     # no para - with return type
#     def add2(self):
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         return res
    
#     # with para - no return type
#     def add3(self,num1,num2):
#         res = num1 + num2
#         print(f'Addition :{res}')

#     # with para - with return type
#     def add4(self,num1,num2):
#         res = num1 + num2
#         return res

# t1 = Test()
# t1.add1()
# x = t1.add2()
# print(f'Addition :  {x}')
# t1.add3(200,100)
# y = t1.add4(200,100)
# print(f'Addition : {y}')

# Example - 3
# Instance Variables
# __init__() called as constructor
# it will execute only once
# when ever we create object, automatically contrsuctor will execute
# class Test:
#     def __init__(self):
#         self.num1 = 10
#         self.num2 = 20

# t1 = Test()
# t2 = Test()
# t1.num1 = 100
# t1.num2 = 200

# print(f't1 object data : {t1.num1}...{t1.num2}')
# print(f't2 object data : {t2.num1}...{t2.num2}')

# Example - 4
# class variables, shared to multiple objects
# class Test:
#     company = "TCS....!"  # class variable

#     def __init__(self,name):
#         self.name = name

# t1 = Test("Emp1")
# print(f'name of the employee {t1.name} and company name {t1.company}')
        
# t2 = Test("Emp2")
# print(f'name of the employee {t2.name} and company name {t2.company}')

# Example - 5
# we can modify class variable with Class Name
# class Test:
#     name = "TCS...!"

# t1 = Test()
# t2 = Test()
# print(f'Name ... {t1.name}')
# print(f'Name...{t2.name}')

# Test.name = "Oracle...!"
# print(f'Name ... {t1.name}')
# print(f'Name...{t2.name}')

# Example - 6
# class Test:
#     name = "Microsoft...!"

# t1 = Test()
# t2 = Test()
# print(f'Name ... {t1.name}')
# print(f'Name...{t2.name}')

# t1.name = "Google" # add instance variable to t1 object
# print(f'Name ... {t1.name}')
# print(f'Name...{t2.name}')

# Example-7
# class Test:
#     company = "TCS...!"
#     def __init__(self,name):
#         self.name = name

#     @classmethod
#     def change_company(cls,new_company):
#         cls.company = new_company

# Test.change_company("Oracle...!")
# t1 = Test("Google")
# t2 = Test("Microsoft")

# print(f'Company ... {Test.company}')
# print(f'Company...{Test.company}')

#Example-8
#first pri - object level, next priority -- class level
# class Test:
#     name = "hello" # class var

#     def __init__(self,name):
#         self.name = name
        

# t1 = Test("Samp1")
# print(t1.name)

#Example-9
#__ is used to declare the private variables
#Encapsulation
#private variables, unable to access outside of class
#private variables, unable to access with class objects
# class Test:
#     def __init__(self):
#         self.__amount = 50000
#     def display_amount(self):
#         return self.__amount
    
# t1 = Test()
# # t1.__amount
# print(t1.display_amount())
# print(t1._Test__amount)

#Example-10
# class Parent:
#     def test1(self):
#         print("Parent...!")

# class Child(Parent):
#     def test2(self):
#         print("Child...!")

# obj = Child()
# obj.test1()
# obj.test2()

#Example-11
#Multi Level
# class Parent:
#     def test1(self):
#         print("Parent....!")

# class Child(Parent):
#     def test2(self):
#         print("Child....!")

# class Subchild(Child):
#     def test3(self):
#         print("Subchild....!")
# obj = Subchild()
# obj.test1()
# obj.test2()
# obj.test3()

# Example-12
# Multiple Inheritance
# class Parent1:
#     def test(self):
#         print("Parent1 !!!")

# class Parent2:
#     def test(self):
#         print("Parent2 !!!")

# class Child(Parent1,Parent2):
#     pass

# obj = Child()
# obj.test()

# Ploymorphism
# Behaves like many
# overloadiong
# overriding

# Example - 13
# overriding
# overriding parent class functionality with child class functionality
# class Parent:
#     def db_conn(self):
#         print("SQL Conn Soon...!")

# class Child(Parent):
#     def db_conn(self):
#         print("NoSQL Conn Soon...!")

# obj = Child()
# obj.db_conn()

# obj = Parent()
# obj.db_conn()

# Example-14
# Overloading
# class Test:
#     def addition(self,a,b=0,c=0):
#         print( a+b+c )

# obj = Test()
# obj.addition(10)
# obj.addition(10,20)
# obj.addition(10,20,30)

# Example-15
# Overloading
# class Test:
#     def addition(self,*args): 
#         print(args)

# obj = Test()
# obj.addition(10,10)
# obj.addition(10,20)
# obj.addition(10,20,30)
# obj.addition(10,20,30,40)

# Example-16
# Overloading
# class Test:
#     def addition(self, num1=None, num2=None, num3=None):
#         if num1 and num2 and num3:
#             print(num1 + num2 + num3)
#         elif num1 and num2:
#             print(num1 + num2)
#         elif num1:
#             print(num1)
#         else:
#             print(0)
# obj = Test()
# obj.addition(10)
# obj.addition(10,20)
# obj.addition(10,20,30)
# obj.addition()

#Examle-17
# class Number:
#     def __init__(self, num1):
#         self.num1 = num1

#     def __add__(self, other):
#         return self.num1 + other.num1   # fixed here

# n1 = Number(10)
# n2 = Number(20)

# print(n1 + n2)

#Example-18
#Dunder Methods
# class Test:
#     def __str__(self):
#         return "Wecome"
# obj = Test()
# print(obj)

#Example-19
#abstract method
# from abc import ABC,abstractmethod
# class Business(ABC):
#     @abstractmethod
#     def start_business(self):
#         pass

# class Friend(Business):
#     def start_business(self):
#         print("Initiate AI Startup Company")

# obj = Friend()
# obj.start_business()

#Example-20
#child class function calling parent class func (super())
# class Parent:
#     def test1(self):
#         print("hello")

# class Child(Parent):
#     def test2(self):
#         super().test1()
    
# obj = Child()
# obj.test2()

#Exmple-21
#Child class constructor calling Parent class constructor
# class Parent:
#     def __init__(self,param1):
#         self.param1 = param1

# class Child(Parent):
#     def __init__(self, param1,param2):
#         super().__init__(param1)
#         self.param2 = param2

# obj = Child(200,100)
# print(obj.param1 + obj.param2)

# static methods
# won't use "self" and "cls"
# inside the class with the help os @staticmethod
# we will call with the help of "Class Names"
# utility methods (general purpose methods Ex. validations,....)

# Example-22
# class Test:
#     @staticmethod
#     def greet():
#         print('welcome to static methods !!!')


# Test.greet()

# Example-23
# class MathUtils:
#     @staticmethod
#     def square(num1):
#         return num1*num1
#     @staticmethod
#     def cube(num1):
#         return num1*num1*num1
    
# print(MathUtils.square(10))
# print(MathUtils.cube(20))

"""
            instance            cls            static

self         yes                no               no

cls          no                yes               no

usecase      object            class             common logic / utility logic / helper logic
             related           related
             task              task

             
decorarator no                @classmethod       @staticmethod


access      yes               no                  no
object
data
             
"""

# class Test:
#     # class level variable
#     cmp_name = "Oracle...!"

#     #constructor
#     def __init__(self,name):
#         self.name = name

#     #instance method
#     def test1(self):
#         print(self.name)

#     #class method
#     @classmethod
#     def change_cmp_name(cls,new_cmp):
#         cls.cmp_name = new_cmp

#     #static method
#     @staticmethod
#     def is_major(age):
#         return age>=18
    
# obj = Test("Emp1")
# obj.test1()         # calling instance methods

# Test.change_cmp_name("Microsoft...!")
# print(Test.cmp_name)    #calling class level data

# # obj.change_cmp_name("Microsoft...!") # works, but not suggested

# print(Test.is_major(20)) # call the static methods

# class
# Object
# instance
# cls
# static
# abstract
# inheritance
# polymorphism
# super()



        






