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
                                                            
def test_func(param1,param2,param3="Hello",param4="welcome",*param5,**param6):
    print(param1,param2,param3,param4,param5,param6)

# test_func(10,20,30,40,50,60,70,80,90,name="Samba")
# test_func(param1=10,param2=20)
# test_func(param1=10,param2=20,param3=30,param4=40)
# test_func(param1=10,param2=20,param3=30,param4=40,param5=(10,20,30,40,50))

# def test_func(param1,param2,param3="Hello",param4="welcome",param5=(),**param6):
#     print(param1,param2,param3,param4,param5,param6)
# test_func(param1=10,param2=20,param3=30,param4=40,param5=(10,20,30,40,50))
# test_func(param1=10,param2=20,param3=30,param4=40,param5=(10,20,30,40,50),name="Samba",age=40)