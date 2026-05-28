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
def test_func(param1="Hello"):
    print(param1)

test_func()
test_func("Welcome")
test_func(None)