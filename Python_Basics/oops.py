"""
    class:
        collection of "variables and functions" called as class
        "class" is the keyword, used to declare the class
        "pass" is the keyword, used to create "empty" class
        "constructors" are used to "declare data / initilize data" dynamically
        __init__(), used to declare the constructor
"""
# class Test:
#     pass

# obj1 = Test()
# print(id(obj1))
# print(obj1)

# class Test:
#     def __str__(self):
#         return "Hello"
# obj = Test()
# print(obj)


# class Test:
#     def __init__(self):
#         self.sub = "Agentic AI"

# obj1 = Test()
# obj1.sub = "Super AI"

# obj2 = Test()


# print(obj1.sub)
# print(obj2.sub)


# class Test:
#     def __init__(self,param1,param2):
#         self.id = param1
#         self.sub = param2

# obj1 = Test(111,"Agentic AI")

# obj2 = Test(222,"Super AI")

# obj3 = Test(333,"Quantum Computing")
# print(obj1.id, obj1.sub)
# print(obj2.id, obj2.sub)
# print(obj3.id, obj3.sub)


# class Test:
#     def db_conn(self):
#         print("chromadb conn soon...!")
# obj = Test()
# obj.db_conn()


# class Test:
#     # no para - no return type
#     def add1(self):
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         print(res)
#     # with para - no return type
#     def add2(self,param1,param2):
#         res = param1 + param2
#         print(res)
#     # no para - with return type

#     # with para - with return type

# obj = Test()
# obj.add1()
# obj.add2(200,100)


# class Test:
#     def __init__(self):
#         self.wish = "Hello"
#         print("1:",self.wish)
#     def greet(self):
#         print("2:",self.wish)
# obj = Test()
# obj.greet()

# inheritance - getting the data from Parent class to Child class
# 1) single-level 2) multi-level 3) multiple 4) hirarichal 5) hybrid
# single-level

# class Parent:
#     def __init__(self):
#         self.subject = "AI"
# class Child(Parent):
#     def __init__(self):
#         super().__init__()
#         self.msg = "Hello"
# obj = Child()
# print(obj.subject)
# print(obj.msg)

# class Parent:
#     def __init__(self,num1):
#         self.num1 = num1
# class Child(Parent):
#     def __init__(self, num1,num2):
#         super().__init__(num1)
#         self.num2 = num2
# obj = Child(200,100)
# print(f"Addition : {obj.num1 + obj.num2}")

# class Parent:
#     def test_func1(self):
#         print("welcome to parent !!!")
# class Child(Parent):
#     pass

# obj = Child()
# obj.test_func1()

# class Parent:
#     def __init__(self,param1):
#         self.param1 = param1     # Hello
#     def test_func(self):
#         return self.param1      # Hello
# class Child(Parent):
#     def __init__(self, param1):
#         super().__init__(param1)
#     def test_func(self):
#         return super().test_func()
# obj = Child("Hello")
# print(obj.test_func())



# class Parent:       # test_func1()
#     def test_func1(self):
#         print("Parent !!!")
# class Child(Parent):   # test_func1() & test_func2()
#     def test_func2(self):
#         print("Child !!!")
# class Subchild(Child):  # test_func1(), test_func2() & test_func3()
#     def test_func3(self):
#         print("Subchild !!!")

# obj = Subchild()
# obj.test_func1()
# obj.test_func2()
# obj.test_func3()

# class Parent1:
#     def __init__(self):
#         super().__init__()
#         self.x = "Hello"

# class Parent2:
#     def __init__(self):
#         super().__init__()
#         self.y = "Welcome"

# class Child(Parent1, Parent2):
#     def __init__(self):
#         super().__init__()
#         self.z = "AI"

# obj = Child()
# print(obj.x, obj.y, obj.z)

# __ used to create private members
# private members, we can't access with the help of object
# private members accessable with in the class

# class Test:
#     def __init__(self):
#         self.__msg = "Hello"
#     def test_func(self):
#         return self.__msg

# obj = Test()
# print(obj.test_func())

