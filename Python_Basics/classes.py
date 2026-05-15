# class - collection of variables and functions called as class
# "self" is the predefined keyword, used to refer current class 

# Example-1 (Instance Variable)
# class Test:
#     def __init__(self,num1,num2):
#         self.x = num1
#         self.y = num2

# obj1 = Test(10,20)
# a = obj1.x
# b = obj1.y
# print(a+b)

# obj2 = Test(100,200)
# print(obj2.x + obj2.y)

# Example-2 (Instance Method)
# class Test:
#     def func_one(self):
#         print("Hello")

# obj = Test()
# obj.func_one()

# Example-3 (Instance Methods)
# class Test:
#     # no parameter - no return type
#     def square1(self):
#         num1 = 100
#         res = num1 * num1
#         print(res)
#     # no parameter - with return type
#     def square2(self):
#         num1 = 100
#         res = num1 * num1
#         return res
#     # with parameter - no return type

#     # with parameter - with return type


# obj = Test()
# obj.square1()
# res  = obj.square2()
# print(res)


# Example-4 (Instance Variables & Instance Methods)
# class Test:
#     def __init__(self,num1,num2):
#         self.x = num1
#         self.y = num2

#     def add1(self):
#         print(self.x + self.y)

#     def add2(self):
#         return self.x + self.y

# obj = Test(200,100)
# obj.add1()
# res = obj.add2()
# print(res)

# Example-5 (class variables)
# class Test:
#     company = "Google"
#     def __init__(self,empName):
#         self.empName = empName

# obj1 = Test("Emp1")
# obj2 = Test("Emp2")
# print(obj1.company, obj1.empName)
# print(obj2.company,obj2.empName)

# Test.company = "Microsoft"
# print(obj1.company, obj1.empName)
# print(obj2.company,obj2.empName)


# class Student:
#     # class level variable
#     school_name = "Hyderabad Public School"

#     def __init__(self,sname):
#         self.sname = sname

# obj1 = Student("Student1")
# print(obj1.sname, Student.school_name)

# obj2 = Student("Student2")
# print(obj2.sname,Student.school_name)


# class Employee:
#     comp_name = "TCS"
#     def __init__(self,name):
#         self.name = name

# obj1 = Employee("Emp1")
# print(obj1.name, Employee.comp_name)

# obj2 = Employee("Emp2")
# print(obj2.name,Employee.comp_name)

# Employee.comp_name = "Google"
# print(obj1.name, Employee.comp_name)
# print(obj2.name,Employee.comp_name)

# class Test:
#     name = "Hello"

# obj1 = Test()
# obj1.name = "Welcome" # add instance variable
# print(obj1.name) # access instance variable
# print(Test.name) # access class level variable

# class Test:
#     name = "Hello"

#     @classmethod
#     def my_func(cls,param1):
#         cls.name = param1

# Test.my_func("Welcome")
# print(Test.name)


# class Test:
#     x = 10

# t1 = Test()
# t2 = Test()
# t1.x = 100

# print(t1.x)
# print(t2.x)
# print(Test.x)

# Encapsulation
# class Bank:
#     def __init__(self):
#         self.__balance = 10000
#     def show(self):
#         print(self.__balance)

# b = Bank()
# b.show()

# Inheritance - Single Level Inheritance
# class Parent:
#     def m1(self):
#         print("m1")

# class Child(Parent):
#     pass

# c = Child()
# c.m1()

# Inheritance - Multilevel Inheritance
# class Parent:
#     def m1(self):
#         print("Hello")
# class Child(Parent):
#     def m2(self):
#         print("Welcome")
# class Subchild(Child):
#     def m3(self):
#         print("Gen AI")

# s = Subchild()
# s.m1()
# s.m2()
# s.m3()


# class Parent:
#     def __init__(self):
#         self.num1 = 300

# class Child(Parent):
#     def __init__(self):
#         super().__init__()
#         self.num2 = 200
# class Subchild(Child):
#     def __init__(self):
#         super().__init__()
#         self.num3 = 100

# c = Subchild()
# print(c.num1 +  c.num2 + c.num3)

# class Parent:
#     def __init__(self,num1):
#         self.num1 = num1

# class Child(Parent):
#     def __init__(self, num1,num2):
#         super().__init__(num1)
#         self.num2 = num2

# class Subchild(Child):
#     def __init__(self, num1, num2,num3):
#         super().__init__(num1, num2)
#         self.num3 = num3

# s = Subchild(300,200,100)
# print(s.num1 + s.num2 + s.num3)

# Inheritance (Multiple Inheritance)
# class Father():
#     def money(self):
#         print("Money")

# class Mummy():
#     def gold(self):
#         print("gold")

# class Child(Father,Mummy):
#     pass

# c = Child()
# c.money()
# c.gold()

# Inheritance (Hirarichal)
# class Parent():
#     def m1(self):
#         print("Parent")

# class Child1(Parent):
#     def m2(self):
#         print("Child1")

# class Child2(Parent):
#     def m2(self):
#         print("Child2")

# c1 = Child1()
# c1.m1()
# c1.m2()

# c2 = Child2()
# c2.m1()
# c2.m2()

# Inheritance (hirarichal + multiple) (Hybrid)
# class P1():
#     pass
# class C1(P1):
#     pass
# class C2(P1):
#     pass
# class C3(C1,C2):
#     pass

# Polymorphism (Overriding)
# class Parent():
#     def m1(self):
#         print("Hello")
# class Child(Parent):
#     def m1(self):
#         print("Welcome")

# c = Child()
# c.m1()

# p = Parent()
# p.m1()


from abc import ABC,abstractmethod
class Test1(ABC):
    @abstractmethod
    def m1(self):
        pass

class Test2(Test1):
    def m1(self):
        print("Hello")

t = Test2()
t.m1()