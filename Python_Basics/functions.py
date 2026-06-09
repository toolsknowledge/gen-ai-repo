# no parameters - no return type
# def db_conn():
#     username = "admin"
#     password = "admin@123"
#     res = "Login Success" if username=="admin" and password == "admin@123" else "Login Fail"
#     print(res)

# # call the function
# db_conn()

# with parameters - without return type
# def db_conn(username,password):
#     res = "Login Success" if username=="admin" and password == "admin@123" else "Login Fail"
#     print(res)

# db_conn("admin","admin@123")  

# no para - with return type
# def db_conn():
#       username = "admin"
#       password = "admin@123"
#       res = "Login Success" if username=="admin" and password == "admin@123" else "Login Fail"
#       return res

# x = db_conn()
# print(x)

# with para - with return type
# def db_conn(username,password):
#     res = "Login Success" if username=="admin" and password == "admin@123" else "Login Fail"
#     return res    

# x = db_conn("admin","admin@12")
# print(x)

# square of a number (4 types)


# default parameters
# def test_func(param1=100,param2=200):
#     print(param1,param2)

# test_func()
# test_func(1000,2000)
# test_func(param2=20000)
# test_func(param1=10000)
# test_func(None)
# test_func(param1=20000,param2=None)


# def test_func(param1,param2,param3="Hello",param4="welcome"):
#     print(param1,param2,param3,param4)

# test_func(None,None,None,None)
# test_func(param4=400,param1=100,param3=300,param2=200)
# test_func(None,None)
# test_func(param2=100,param1=200)
# test_func() #TypeError: test_func() missing 2 required positional arguments: 'param1' and 'param2'
# test_func(100,200)

# Note : all the default parameters are at the end of function declaration
# def test_func(x,z,y=10,a=20):
#     pass

# variable-length arguments
# def test_func(*param1):
#     print(param1)

# test_func(10)
# test_func(10,20,30,40,50)
# test_func("Hello","Welcome")

# Note : we are unable to pass two variable-length parameters
# def test_func(*param1,*param2):
#     pass

# def test_func(param1,param2="Hello",*param3):
#     print(param1,param2,param3)

# test_func(10,20,30,40,50,60,70,80,90,100)
# test_func(param1=100,param2=200,param3=(10,20))


# def test_func(**param1):
#     print(param1)

# test_func(name="Samba",age=40)


# def test_func(param1,param2="Hello",*param3,**param4):
#     print(param1, param2, param3, param4)

# test_func(10,20,30,40,50,name="Samba",age=40)

# tuple - () store multiple values
# {} -- key & value pairs



# lambda
# res = lambda num1: num1*num1
# x = res(10)
# print(x)

# res = lambda num1,num2: num1+num2
# x = res(200,100)
# print(x)

"""
    map() - manipulate every list element
                map()
    [1,2,3,4,5] --> [10,20,30,40,50]
"""

# res = list(map(lambda num1:num1*num1, [1,2,3,4,5]))
# print(res)

# res = list(map(lambda num1,num2:num1+num2,[1,2,3],[10,11,12]))
# print(res)


# [100,200] [10,20]  --> [90,180]
# [1,2,3] [4,5,6] [7,8,9] --> [12,15,18]


# res = list( filter(lambda num1:num1%2 == 0,[1,2,3,4,5]) )
# print(res)

# [1,2,3,4,5] = 15  reduce()
from functools import reduce
res = reduce(lambda num1,num2:num1+num2,[1,2,3,4,5])
print(res)







# Function
# particular business logic called as Function
#       (or)
# set of instructions also called as Function
# "def" is the keyword, used to declare the Function
# "pass" is the keyword, representing "empty" function

# no para - no return type
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     print(res)

# addition()

# no para - with return type
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     return res

# x = addition()
# print(x)


# with para - no return type
# def addition(num1,num2):
#     res = num1 + num2
#     print(res)

# addition(200,100)

# with para - with return type
# def addition(num1,num2):
#     res = num1 + num2
#     return res

# x = addition(200,100)
# print(x)


# multiplication
# no para - no return type
# no para - with return type
# with para - no return type
# with para - with return type

# default parameters
# def test_func(param1="Hello"):
#     print(param1)

# test_func()
# test_func("Welcome")
# test_func(None)

# def test_func(param1="Hello",param2="Welcome"):
#     print(param1,param2)

# test_func()
# test_func(100,200)
# test_func(param2="Python")
# test_func(param1="Gen AI")
# test_func(param2="Agentic AI",param1="FastAPI")

# def test_func(param1,param2,param3="Hello"):
#     print(param1, param2, param3)

# test_func(100,200)
# #test_func()
# test_func(100,200,300)
# test_func(param2="Gen AI",param1="Agentic AI")
# test_func(param3=3,param2=2,param1=1)
# test_func(None,None,None)

# def test_func(*param1):
#     print(param1)
#     print(type(param1))

# test_func(10,20,30,40,50)
# test_func("Python","FastAPI","Gen AI","Agentic AI","Deployment")
# test_func(None)


# Note : function, allows only one tuple parameter
# def test_func(*param1,*param2):
#     pass

# def test_func(*param1,param2="Hello",param3):
#     print(param1,param2,param3)
# test_func(param3="Hello")


# def test_func(param1,param2,param3="Hello",param4=()):
#     # param1, param2 - normal
#     # param3 - default
#     # param4 - tuple
#     print(param1, param2, param3, param4)

# test_func(10,20,30,40,50,60,70)
# t1 = (10,20,30,40,50,60)
# test_func(10,20,30,*t1)

# test_func(param1=10,param2=20,param3=30,param4=t1)

# def test_func(**param1):
#     print(param1)
#     print(type(param1))
# test_func(name="Samba",age=40)

# Note: it wont allows two dict parameters
# def test_func(**param1,**param2):
#     pass
                                                            
# def test_func(param1,param2,param3="Hello",param4="welcome",*param5,**param6):
#     print(param1,param2,param3,param4,param5,param6)

# test_func(10,20,30,40,50,60,70,80,90,name="Samba")
# test_func(param1=10,param2=20)
# test_func(param1=10,param2=20,param3=30,param4=40)
# test_func(param1=10,param2=20,param3=30,param4=40,param5=(10,20,30,40,50))

# def test_func(param1,param2,param3="Hello",param4="welcome",param5=(),**param6):
#     print(param1,param2,param3,param4,param5,param6)
# test_func(param1=10,param2=20,param3=30,param4=40,param5=(10,20,30,40,50))
# test_func(param1=10,param2=20,param3=30,param4=40,param5=(10,20,30,40,50),name="Samba",age=40)