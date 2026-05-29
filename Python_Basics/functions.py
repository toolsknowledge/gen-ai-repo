"""
    functions
    *********
        set of instructions called as functions
             (or)
        particular "business logic" also called as function
        
        functions are used to "reuse" business logic

        "def" is the keyword, used to declare the function

        "pass" is the keyword, used to create "empty functions"
"""
# no para - no return type
# def addition():
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         print(res)                  #300

# addition()

# no para - with return type
# def subtraction():
#     num1 = 200
#     num2 = 100
#     res = num1 - num2
#     return res

# x = subtraction()
# print(x)

# with para - no return type
# def multiply(num1,num2):
#     res = num1 * num2
#     print(res)

# multiply(200,100)

# with para - with return type
# def division(num1,num2):
#     res = num1 / num2
#     return res

# x = division(200,0)
# print(x)

# with para - with return type
# def login(uname,pwd):
#     #res = "success" if uname=="admin" and pwd=="admin@123" else "fail"
#     res=""
#     if uname=="admin" and pwd=="admin@123":
#         res = "success"
#     else:
#         res = "fail" 
    
#     return res

# res = login("admin","admin@123")
# print(res)

# default parameters
# def test_func(param1="Hello"):
#     print(param1)

# test_func()
# test_func("Welcome")
# test_func(None)

# def test_func(num1,num2=10):
#     return num1 + num2

# print(test_func(5))
# print(test_func(10,20))

# default parameters order must be last in parameters list
# def test_func(param1="Hello",param2):
#     pass
    
# in case of list, modified list will be used in next iterations
# def test_func(x=[]):   
#     x.append(1)
#     return x

# print(test_func()) # [1]
# print(test_func()) # [1,1]
#                    # [1,1,1]


# def test_func(x=None):
#     if x is None:
#         x = []
#     x.append(1)
#     return x

# print(test_func())
# print(test_func())


# by default int is immutable
# for every call num1 will be "5"
# def test_func(num1=5):
#     num1 += 1
#     return num1
# print(test_func())
# print(test_func())

# default parameters are initilized while declaraing the functions
# num1 = 100
# def test_func(param1 = num1):
#     print(param1)

# num1 = 200
# test_func()

# def test_func(sub="Gen AI",version=2):
#     print(sub,version)

# test_func(version=3,sub="Agentic AI")


# variable length arguments
# def test_func(*param1):   
#     print(param1)
#     print(type(param1))

# test_func(10,20,30,40,50)

# param1 - non default
# param2 - variable length (tuple)
# param3 - default parameter

# def test_func(param1,*param2,param3="Hello"):
#     print(param1,param2,param3)

#test_func() #TypeError: test_func() missing 1 required positional argument: 'param1'
#test_func(10) #10 () Hello
#test_func(10,20,30,40,50) #10 (20, 30, 40, 50) Hello
#test_func(10,20,param3="Welcome") #10 (20,) Welcome
#test_func(100, 10, 20, 30, 40, 50, param3="Python")


# we are able to pass only one tuple per function
# def test_func(*param1,*param2):
#     pass


def test_func(**param1):
    print(param1)

test_func(name="Samba",sub="Gen AI")









