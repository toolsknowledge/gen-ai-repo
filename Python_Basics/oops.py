# OOPS
# LIST
# TUPLES
# SET
# DICTIONARY
# NUMPY
# PANDAS
# MATPLOTLIB
# SEABORN

# FAQ8: isinstance vs type
# class A:
#     pass
# class B(A):
#     pass
# obj = B()
# print(isinstance(obj,A)) #true
# print(isinstance(obj,B)) #true
# print(type(obj) == B) # True
# print(type(obj) == A) # False


# FAQ7: Modify Class Variable
# class Test:
#     x = 10

# t1 = Test()
# t2 = Test()
# Test.x = 100
# print(t1.x)
# print(t2.x)


# FAQ6: MRO (Method Resolution Order)
# class A:
#     def show(self):
#         print("A")

# class B(A):
#     def show(self):
#         print("B")

# class C(A):
#     def show(self):
#         print("C")

# class D(C,B):
#     pass

# d = D()
# d.show()




# FAQ5: constructor with return
# class Test:
#     def __init__(self):
#         return "Hello"
# obj = Test() #Err


# FAQ4: private variables
# class Test:
#     def __init__(self):
#         self.__x = 100
#     def display(self):
#         return self.__x

# t1 = Test()
# #print(t1.__x) # Err
# print(t1._Test__x)
# print(t1.display())


# FAQ3: Overriding
# class A:
#     def show(self):
#         print("A")
# class B(A):
#     def show(self):
#         print("B")
# obj = B()
# obj.show()

# obj1 = A()
# obj1.show()





# FAQ2 : Mutable Argument Trap
# class Test:
#     def __init__(self,items=[]):
#         self.items = items

# t1 = Test()
# t1.items.append(100)

# t2 = Test()
# print(t2.items)



# FAQ1
# class Test:
#     x = 10   # class variable

# t1 = Test()
# t2 = Test()
# t1.x = 100
# print(t1.x)
# print(t2.x)




# # Duck Typing
# class Test1:
#     def test1(self):
#         print("Hello....Soon we will start ML")
# class Test2:
#     def test1(self):
#         print("Hello....soon qwe will start Gen AI")
# def my_test_func(obj):
#     obj.test1()

# obj1 = Test1()
# my_test_func(obj1)

# obj2 = Test2()
# my_test_func(obj2)





# class Number:
#     def __init__(self,x):
#         self.x = x

#     def __add__(self, other):
#         return self.x + other.x

# obj1 = Number(10)
# obj2 = Number(20)
# print(obj1 + obj2)  # obj1.__add__(obj2)




# from abc import ABC,abstractmethod

# class Parent(ABC):
#     @abstractmethod
#     def test1(self):
#         pass

# class Child(Parent):
#     def test1(self):
#         print("welcome to test1 !!!")

# obj = Child()
# obj.test1()







# class Calc:
#     def add(self,num1,num2,num3=0):
#         print(num1 + num2 + num3)

# obj = Calc()
# obj.add(200,100)
# obj.add(300,200,100)





# class Parent:
#     def __init__(self,name):
#         self.name = name

# class Child(Parent):
#     def __init__(self, name, age):
#         super().__init__(name)
#         self.age = age

# obj = Child("Std1",20)
# print(obj.name)
# print(obj.age)





# class Parent:
#     def ora_conn(self):
#         return "oracle connection soon...!"
    
# class Child(Parent):
#     def mysql_conn(self):
#         return "mysql connection soon...!"

# class Subchild(Child):
#     def mongodb_conn(self):
#         return "mongodb connection soon...!"

# obj = Subchild()
# res1 = obj.ora_conn()
# print(res1)

# res2 = obj.mysql_conn();
# print(res2)

# res3 = obj.mongodb_conn()
# print(res3)


# class Parent:
#     def test1(self):
#         print("test1")

# class Child(Parent):
#     def test2(self):
#         print("test2")


# c = Child()
# c.test1()
# c.test2()





# class Test:
#     x = 10

# t1 = Test()
# t2 = Test()

# Test.x = 20;
# t1.x = 30
# print(Test.x, t1.x,t2.x)




# class Test:
#     x = 10

# t1 = Test()
# t2 = Test()
# t1.x = 20

# print(t1.x,Test.x)

# print(t2.x)




# class Student:
#     name = "AshokIT"

#     @classmethod
#     def change_name(cls,new_name):
#         cls.name = new_name

# s1 = Student()
# print(s1.name)
# s2 = Student()

# Student.change_name("AshokIT-DataScience")
# print(s1.name)
# print(s2.name)



# class Student:

#     name = "AshokIT"

#     @classmethod
#     def test_func(obj):
#         print(obj.name)

# Student.test_func()



# class Student:
#     # class variables
#     msg = "AshokIT"

#     def __init__(self,name):
#         self.name = name

# s1 = Student("Std1")
# print(s1.name, s1.msg)

# s2 = Student("Std2")
# print(s2.name,s2.msg)






# class Student:
#     def __init__(self,name,age,marks,grade):
#         self.name = name
#         self.age = age
#         self.marks = marks
#         self.grade = grade

#     def display(self):
#         print(self.name,self.age,self.marks,self.grade)

# s1 = Student("Std1",20,90,"A")
# s1.display()





# instance variables
# class Student:
#     def __init__(self,name,age):
#         self.name = name
#         self.age = age

# s1 = Student("Std1",20)
# print(s1.name,s1.age)
# s2 = Student("Std2",22)
# print(s2.name,s2.age)






# class Student:
#     def __init__(self):
#         print("Constructor Called")

# s1 = Student()




# class Student:
#     pass

# s1 = Student()
# print(type(s1))