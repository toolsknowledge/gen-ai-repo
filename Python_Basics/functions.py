# from functools import reduce
# print( reduce(lambda x,y:x+y,[1,2,3,4,5]) )

# reduce() --> used to find the sum of list elements
# filter() --> used to apply the condidions
# map() ---> manipulate every list element
# res=0
# for num in [1,2,3,4,5]:
#     res=res+num
# print(res)
# print(sum([1,2,3,4,5]))




# print(list(filter(lambda x:x>10,[10,20,30,40,50])))


# print( list( map(lambda num:num*num,[1,2,3,4,5]) ) )

# numbers = [1,2,3,4,5]
# def square(num):
#     return num*num
# result = map(square,numbers)
# print(list(result))




# FAQ'S (NEW - DIFF)
# BASIC --> FAQ'S. (Duration) (1.15min / 1.30min)


# def test_func1(num1):
#     return num1 * num1

# def test_func2(func,value):
#     return func(value)

# print( test_func2(test_func1,5) )



# x = 10
# def test_func():
#     global x
#     x = 100

# test_func()
# print(x)




# x = 10 # global
# def test_func():
#     x = 5 # local
#     print(x)

# test_func() #5
# print(x) #10




# def outer(num1):
#     def inner(num2):
#         return num1+num2
    
#     return inner

# x = outer(200)
# res = x(100)
# print(res)

# def outer():
#     def inner():
#         print("Hello,AshokIT")
    
# outer()





# res = lambda num1,num2:num1+num2
# x = res(200,100)
# print(x)

# res = lambda num1:num1*num1
# x = res(4)
# print(x)

# def factorial(n):
#     if n==1:
#         return 1
#     return n * factorial(n-1)   # 5 * factorial(4)
#                                 # 5 * 4 * factorial(3)
#                                 # 5 * 4 * 3 * 2 * 1
#                                 # 120
                               

# print(factorial(5))




# def test_func():
#     return 100,200,300

# res = test_func()
# num1,num2,num3 = res
# print(type(num1),num2,num3)



# def test_func(**param1):
#     print(param1)

# test_func(name="AshokIT",course="AIML")





# Arbitrary Arguments
# "*"
# def test_func(*nums):
#     print(sum(nums))
#     print(len(nums))
#     print(max(nums))
#     print(min(nums))

# test_func(10,20,30,40,50)


# keyword arguments
# def test_func(name,age):
#     print(name, age)

# test_func(age=40,name="Shiva")
# test_func("Hello",20)





# Default Parameters
# def test_func(param1="Hello",param2="Welcome"):
#     print(param1, param2)

# test_func()             #Hello Welcome
# test_func(100,200)      #100 200
# test_func(None,1000)    #None 1000




# no para - no return type
# no para - with return type
# with para - no return type
# with para - with return type



# def db_func(username,password):
#     if(username == "scott" and password == "tiger"):
#         return "Login Success"
#     else:
#         return "Login Fail"

# res = db_func("scott","tiger")
# print(res)

# def db_func(username,password):
#     if(username=="scott" and password=="tiger"):
#         print("Login Success")
#     else:
#         print("Login Fail")

# db_func("scott","tiger")






# def db_func():
#     username = "AshokIT"
#     password = "AshokIT@123"
    
#     if(username=="AshokIT" and password=="AshokIT@123"):
#         return "Login Success"
#     else:
#         return "Login Fail"

# res = db_func()
# print(res)




# def db_func():
#     username = "admin"
#     password = "admin@123"

#     if(username == "admin" and password == "admin@123"):
#         print("Login Success")
#     else:
#         print("Login Fail")

# db_func()


# def test_func():
#     print("welcome to functions !!!")

# test_func()