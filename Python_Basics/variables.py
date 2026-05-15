# variables are used to "store the data"
# Ex.int, str, bool, None,....
# Rule1 : a-z, A-Z, 0-9, $ and _
# Rule2: variable declaration should not start with "digits" 

# number -- int, float, complex
# int
# num1 = 100
# num2 = -100
# num3 = 0
# print(num1,num2,num3)
# print(type(num1)) #<class 'int'>

# float
# f1 = 10.1
# f2 = -10.2
# print(f1, f2)
# print(type(f1)) #<class 'float'>

# complex
# Electrical  AC - vol, phase
# num = 3 + 4j
# print(num.real)
# print(num.imag)
# print(type(num)) #<class 'complex'>


# num1 = 100
# float() is the predefined function, used to convert int to float
# num2 = float(num1)
# print( type(num2) )


# num1 = 15.1222222222
# num2 = int(num1)   #int() is the predefined function, used to convert float to int
# print(type(num2))   #<class 'int'>

# num1 = 10
# num2 = complex(num1)  # complex() is the predefined function, used to convert int/float to complex
# print(num2)     #(10+0j)

# num1 = 200
# num2 = 100
# add = num1 + num2
# print(add)

# sub = num1 - num2
# print(sub)

# mul = num1 * num2
# print(mul)

# div = num1 / num2
# print(div)

# fdiv = num1 // num2
# print(fdiv)

# modulus = num1 % num2
# print(modulus)

# print(2 ** 3)
# print(round(5.45))
# print(max(10,20,30))
# print(min(10,20,30))
# print(num1 > num2)
# print(num1 < num2)
# print(num1 == num2)

# string - collection of characters called as string
# 1) "" (double quotes) 2) ''(single quotes) 3) """ """ (triple quotes)
# """ """ (triple quotes) - used to represent multi line string
# string is immutable


# str1 = "Machine Learning"
# str2 = 'Deep Learning'
# str3 = """
#         Agentic AI
#         Generative AI
# """
# print(str1)
# print(str2)
# print(str3)

# Format
# sub = "Python"
# wish = "Welcome to %s" %sub
# print(wish)

# name = "Student1"
# age = 9
# str = "Student name is {} and age is {}".format(name,age)
# print(str)

# sub = "Agentic AI"
# wish = f"welcome to {sub}"
# print(wish)

# str = "welcome"
# print(str[0], str[-7])
# print(str[0:3])         # 0 will include and 3 will excluded
# print(str[:2])          # 0:2
# print(str[2:])          # 2nd index to last
# print(str[-4:])         # -4 index to last index
# print(str[::-1])        # reverse the string
# print(str[::2])         # wloe
# print(str[1::2])        # ecm
# print(str[-7:-4][::-1]) #lew


# len() - number of characters
# str = "Python"
# print(len(str))

# upper() - lower case characters to upper case characters
# str = "python"
# print(str.upper())

# lower() - upper case character to lowercase case characters
# str = "PYTHON"
# print(str.lower())

# title() - first letter converts to capital
# str = "welcome to python"
# print(str.title())

# strip() - remove white spaces
# str = " python "
# print(str.strip())

# replace() - replace operation
# str = "java is eazy"
# print( str.replace("java","python") )

# split() - split operation
# str = "python is eazy"
# print(str.split(" "))

# join() - list - string
# list1 = ['python', 'is', 'eazy']
# print(" ".join(list1))

# in (membership operator)
# str = "python is eazy"
# print("python" in str)
# print("java" in str)

# == (comparision)
# print("python" == "python")
# print("python" == "PYTHON")

# Escape (\n) (\t)
# print("welcome to\npython")
# print("welcome to\tpython")
# print("welcome to \"python\"")
# print("welcome to \'python\'")

# Concatination
# str1 = "welcome"
# str2 = "to"
# str3 = "python"
# wish = str1+" "+str2+" "+str3
# print(wish)

# repeat
# str1 = "python"
# print(str1 * 5)

# print("python" > "java")

# str = "python"
# print(str.find("p")) # 0
# print(str.find("P")) # -1


# str = "AgenticAI"
# print(str.index("A")) #0
# print(str.index("a")) #ValueError: substring not found

# Boolean
# True & False
# Case Sensitive
# True - 1  False - 0

# flag1 = True
# print(flag1) # True

# flag2 = False
# print(flag2) # False

# print(type(flag1)) # <class 'bool'>

# flag3 = true
# print(flag3) # NameError: name 'true' is not defined.

# flag4 = false
# print(flag4) # NameError: name 'false' is not defined.

# Comparision Oprerators 1) ==,  2) !=  3) >  4) <  5) >= 6) <=
# print(100 == 100, end=" ")
# print(100 != 100, end=" ")
# print(100 > 100, end=" ")
# print(100 >= 100, end=" ")
# print(100 < 100, end=" ")
# print(100 <= 100)

# False
# print(bool(0))
# print(bool(None))
# print(bool(""))
# print(bool([]))  # ["Shaik Chand","Agentic AI","8PM"] list [] mutable
# print(bool({}))  # {"name":"Madhuri"}  dict {}
# print(bool(()))  # ["Shaik Chand","Agentic AI","8PM"] tuple () immutable
# print(bool(set())) # wont allows duplicates 10,10  10

# True
# print(bool(1))
# print(bool(100))
# print(bool(-100))
# print(bool("Hello"))
# print(bool([10,20,30,40,50]))
# print(bool((10,20,30)))
# print(bool("False")) 
# print(bool(set([10,10,10])))
# print(bool({"name":"abc"}))

# And 
# print(True and True)
# print(True and False)
# print(False and False)
# print(False and True)

# OR
# print(True or True)
# print(True or False)
# print(False or False)
# print(False or True)

# not
# print(not True)
# print(not False)

# print(True + True)
# print(1 + True)
# print(1 + 1 + True + False)
# print(True > False)
# print(False > True)
# print(True / False)
# print(False / True)
# print(1 + "True") #TypeError

# print(True == 1) # value
# print(True is 1) # datatypes & value

# all() (and) (&)
# print(all([10>9, 5>4, 2<3]))

# any() (or) (|)
# print( any([10>90, 50<6, 10>100]) )

# number
# string
# boolean


# None
# DataType in Python
# No value / Empty Value / Missing Value
# Null-like Object
# None != 0 , None !="" , None != False

# x = None
# print(x)
# print(type(x))
# print(None == 0)
# print(None == "")
# print(None == False)


# roll_no = None
# if roll_no is None:
#     print("Roll Number Not Assigned !!!")


# list
# ordered collection
# hetrogeneous elements
# []
# mutable

# list1 = [10,20,30,40,50]
# print(list1[0], list1[-5])
# print(list1[0:3])
# print(list1[-5:-1])
# print(list1[1:])
# print(list1[:2])
# print(list1[::-1])
# print(list1[::-2])

# list1[0] = 1000
# print(list1)

# e1,e2,e3,e4,e5 = list1
# print(e1,e2,e3,e4,e5)
# print(type(e1))

# e1,*list2,e2 = list1
# print(list2)

# for element in list1:
#     print(element)


# tuple
# ordered collection
# immutable(can't modify)
# allows duplicates
# hetrogeneous elements
# ()

# t1 = (10,20,30,40,50)
# print(t1)
# t2 = 100,200,300,400,500
# print(t2)
# t3 = (1,2,3,4,5)
# print(t3[0])
# print(t3[1:3])
# print(t3[:2])
# print(t3[2:])
# print(t3[::-1])

# t4 = (100,200,300,400,500)
# t4[0] = 1000

# t5 = (1,1,2,3,3,3,2,2,2,1)
# print(t5.count(1))
# print(t5.count(2))
# print(t5.count(3))
# print(t5.count(4))
# print(t5.index(1))
# print(t5.index(3))

# t6 = (100,200,300,400,500,600)
# for element in t6:
#     print(element,end=" ")

# t7 = (10,20,30,40,50)
# print(30 in t7)
# print(60 in t7)
# print(30 not in t7)
# print(60 not in t7)

# t8 = (1,2,3)
# print(len(t8))
# print(max(t8))
# print(min(t8))
# print(sum(t8))

# t9 = (10,20,30,40,50)
# e1,*l1,e5 = t9
# e2,*l2 = l1
# e3,e4 = l2
# print(e1,e2,e3,e4,e5)

# t10 = (10,20,30,40,50)
# list1 = list(t10) #list() -- convert tuple to list
# print(list1)
# list1[0] = 1000
# print(list1)
# new_t10 = tuple(list1) #tuple() -- convert list to tuple
# print(new_t10)

# Dictionary
# key - value pairs
# Unordered (older python) , Ordered (Python 3.7+)
# Mutable 
# keys must be unique

# d1 = {
#     "name":"std1",
#     "marks":20
# }
# print(type(d1))
# print(d1.keys())
# print(d1.values())
# print(d1.items())
# for element in d1.values():
#     print(element)
# print(d1["name"])

# Set
# wont allows duplicates
# {}
s1 = {1,1,2,2,3,3}
print(s1)
print(type(s1))

# int
# float
# str
# bool
# list
# None
# tuple
# dict
# set







