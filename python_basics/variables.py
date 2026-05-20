# variable - variables are used to store the data
# Ex. int, float, string, boolean, list, tuple, dict,....
# variable declaration must contain a-z, A-Z, 0-9, $ and _
# variable declaration should not start with digits
# Integer (int) - int, float, complex
# num1 = 100
# num2 = -100
# print(num1)
# print(num2)
# print( type(num1) )

# hexa = 0xA
# print(hexa)
# octa = 0o12
# print(octa)
# bina = 0b1010
# print(bina)

# large = 123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789
# print(large)

# print(10 / 2)
# print(10 // 3)  # Floor Division 3
# print(-10 // 3) # -4
# print(10 % 3) 

# temp = 98.3
# print(temp)
# print(type(temp))

# expo = 2e-4
# print(expo)

# comp1 = 4 + 5j
# print(comp1.real)
# print(comp1.imag)
# print(type(comp1))

# num1 = 10
# float1 = float(num1)
# print(float1)

# float2 = 10.9
# num2 = int(float2)
# print(num2)


# print(max(10,20,30))
# print(min(10,20,30))
# print(divmod(10,3))
# print(pow(2,3))


# string
# collection of characters called as string
# 1) ""    2) ''    3) """"""
# define multi line string, then we will use """"""

# str1 = "Hello"
# str2 = 'welcome'
# str3 = """
#     welcome to Gen AI & Agentic AI
#     we will cover real appln also
#     we will cover deployment also
# """
# print(str1)
# print(str2)
# print(str3)

# name = "Samba"
# age = 40
# print("My name is %s and age is %d" %(name,age))
# print("My name is {} and age is {}".format(name,age))
# print(f"My name is {name} and age is {age}")

# boolean
# True (1) / False (0)
# flag = True
# flag1 = False
# print(flag)
# print(flag1)
# print(True + True)
# print(True / False)
# print(True + 1 + True + False)

# list
# ordered collection of elements
# []
# hetrogeneous elements

# list1 = [10,20,30,40,50]
# print(list1[0])
# print(list1[-5])
# print(list1[0:3])
# print(list1[1:4])
# print(list1[:4])
# print(list1[3:])
# print(list1[::-1])


# tuple
# collection of ordered elements
# ()
# index starts from "0"
# immutable (can't modify)
# t1 = (10,20,30,40,50)
# print(t1[0],t1[-5])
# print(t1[0:3])
# print(t1[-3:-1])
# print(t1[2:])
# print(t1[:2])
# print(t1[::-1])
# print(type(t1))
# t1[0] = 1000

# dictionary
# store the data in the form of "key&value" pairs
# d1 = {
#     "name" : "Std1",
#     "age" : 20,
#     "marks" : 95
# }
# print(d1["name"], d1["age"], d1["marks"])
# print(type(d1))
# print(d1.keys())
# print(d1.values())
# print(d1.items())

# Set
# wont allows "duplicates"
# {}
# unordered collection of elements
# s1 = {10,10}
# print(s1)
# print(type(s1))
# s2 = {10,20,30,10,20,30,"Hello",True,"Hello"}
# print(s2)

# None
# Empty / No Value
# emp1 = None
# print(emp1)
# print(type(emp1))
# emp1 = "EMP001"
# print(emp1)

# DataTypes
# Number - int,float,complex
# String - "", '' and """ """
# Boolean - True - 1, False - 0
# List - collection of ordered elements, [], mutable
# Tuple - collection of ordered elements, (), immutable
# Dictionary - key & value pairs, {}, keys(), values(), items()
# Set - won't allows duplicates,{}
# None - Representing empty / blank / no value

t1 = (10,20,30,40,50)
# list() is the predefined function, used to convert tuple to list
list1 = list(t1)
list1[0] = 1000
# tuple() is the predefined function, used to convert list to tuple
t2 = tuple(list1)
print(t2)

