# collection of variables and functions called as class
# "class" is the keyword, used to declare the class
# __init__, used to declare the constructor
# constructor,used to initilize the instance variables
# instance members are availble in separate copies for each object

class Test:
    # no para - no return type
    def add1(self):
        num1 = 200
        num2 = 100
        res = num1 + num2
        print(res)

    # no para - with return type
    def add2(self):
        num1 = 200
        num2 = 100
        res = num1 + num2
        return res
    
    # with para - no return type
    def add3(self,param1,param2):
        res = param1 + param2
        print(res)
    
    # with para - with return type
    def add4(self,param1,param2):
        res = param1 + param2
        return res

obj1 = Test()
obj1.add1()

x = obj1.add2()
print(x)

obj1.add3(200,100)

y = obj1.add4(200,100)
print(y)

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