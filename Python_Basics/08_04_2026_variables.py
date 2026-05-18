# string
# collection of characters
# "" (double quotes) ,  '' (single quotes) ,  """ """(triple quotes)
# str1 = "Hello,Python"
# str2 = 'Hello, Python Variables !!!'
# str3 = """
#         Hello Team,
#             Welcome to Python
#             Time : 9AM (IST)
# """
# print(str1)
# print(str2)
# print(str3)

# """
#     this is ignored line
# """
# x = 100
# print(x)

# str = "Hello"
# print(str[0], str[-1])
# print(str[-1])
# print(str[0:2])
# print(str[:2])
# print(str[2:])
# print(str[::-1])

# str = "Python" # immutable
# str[0] = "H"


# str = "Python"
# str1 = "p" + str[1:]
# print(str1)

# str1 = "Hello"
# str2 = "World"
# print(str1 +" " +str2)
# print(str1 * 3)

# print("Py" in "Python")
# print("Java" not in "Python")

# print( len("Python") )                      # know number of characters
# print( "HELLO".lower() )                    # converts Uppercase to Lowercase
# print( "hello".upper() )                    # converts lowercase to uppercase
# print( "hello".replace("h","y") )           # perform replacement
# print("welcome to python".split(" "))       # perform split() based on special character
# print(",".join(['welcome', 'to', 'python']).replace(",", " ")) # join

# str = "Python"
# for ch in str:
#     print(ch)

# str = "DataSciencs"
# msg = f"welcome to {str}"
# print(msg) 

# print("Hello\nWorld") #\n - new line
# print("Hello\tWorld") #\t - tab space
# print("Welcome to \"DataScience\"") # include double quotes
# print("it\'s a DataSciencs") # include '
# print("C:\\User\\Python") # include \

# str = "python"
# new_str= str.replace("p","y")
# print(new_str)
# print(str)

# Boolean
# True -- 1
# False -- 0
# flag1 = True
# print(flag1)
# flag2 = False
# print(flag2)
# print(True + 1)
# print(True + False)

age = 18
# if age >=18:
#     print("Major !!!")
# else:
#     print("Minor !!!")

# print( "Major" if age>18 else "Minor" )

# None --> No Value / Nothing / "Empty but not zero"
# x = None
# print(x)
# print(type(x))

# list
# collection of elements
# []
# Hetrogeneous
# Duplicates
# Ordered
# mutable

# list1 = [10,10,"hello",True,10.1,None]
# print(list1)
# list2 = [10,20,30,40,50]
# print(list2[0])
# print(list2[-1])
# list2[0] = 1000
# print(list2)
# print(type(list2))

# tuple
# collection of elements
# ()
# Hetrogeneous
# Duplicates
# Ordered
# immutable
# t1 = (10,10,20,30,10,True,"Hello",10.1,None)
# print(type(t1))
# t1[0] = 1000

# dict
# key & value 
# d1 = {
#     "name" : "DataScience",
#     "sub" : "Gen AI",
#     "cloud" : "MLops, LLOps"
# }
# print(d1["name"])
# d1["sub"] = "Gen AI & Agentic AI"
# del d1["cloud"]
# print(d1)
# print(type(d1))


# Set
# collection of elements
# {}
# no duplicates
# no order
# s1 = {1,1,2,3,1,2,3,None,None}
# print(len(s1))
# print(s1[0])
# print(type(s1))


# s1 = {1,1,2,3,1,2,3,None,True,False}
# print(len(s1))
# print(s1[0])
# print(type(s1))
# print(s1)

# int
# float
# str
# bool
# list
# tuple
# dict
# None
# set


# num1 = 200
# num2 = 100

# addition = num1 + num2
# print(addition)
# print(type(addition)) # int # type() is the predefined func, used to know the datatype

# num3 = 10.5
# num4 = -10.5
# res1 = num3 + num4
# print(res1)
# print(type(res1)) # float
