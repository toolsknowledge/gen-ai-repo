# variables
# store the data Ex. number, string, boolean, list, tuple, dict, ......
# Rule1: a-z, A-Z, 0-9, $ and _
# Rule2 : declaration should not start with "digits"
# Rule3: dont use predefined keywords as variables declration like Ex.if,def,function,return,....
"""
    datatypes

    1) number --- int, float, complex
    2) str
    3) bool
    4) list
    5) tuple
    6) set
    7) dict
    8) NoneType

"""

"""
    1) int
        whole numbers representing "int data" (positive numbers / negative numbers)
        we are able to store "large numbers"
"""
x = 100
y = -100
z = 123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789
print(x)
print(y)
print(z)
print(type(x))


"""
    2) float
"""

f1 = 0.1
f2 = 0.2
f3 = f1 + f2
# f3 = 0.30000000000000004
print(f3)
print(type(f3))

"""
    complex numbers
    1) electrical engineering
    2) signal processing
    3) physics
    4) AI Mathematics
    5) scientific calculations

    Real Part + Imaginary Part
"""
c1 = 3 + 4j
print(c1.real)
print(c1.imag)
print(type(c1))


"""
    string
    ******
        collection of characters
        1) ""
        2) ''
        3) """"""" (define paragraphs)
"""
ai_ver = 2
print("AI Current Trending Version is %d " % ai_ver)

name = "Generative AI"
print("Current Version Name is %s " % name)

price = 99.5
print("Price is %f " % price)

pi = 3.14159
print("%.4f" %pi)

print("%s scored %d rank" % ("Ravi",95))

print("Current Trending Subject is {} and version is {}".format("AgenticAI",2))
print("Current Trending Subject is {1} and version is {0}".format(2,"AgenticAI"))
print("Current Trending Subject is {key1} and version is {key2}".format(key1="AgenticAI",key2=2))

name = "Test"
print(f"Name is {name}")

str = """
    Traditional AI
    Agentic AI
    Super AI
"""
print(str)

"""
    bool
        1) True     - 1
        2) False    - 0
"""
flag = True
res = "Hello" if flag else "Welcome"
print(res)

flag1 = False
res1 = "Hello" if flag1 else "Welcome"
print(res1)


"""
    list
    ****
        collection of "hetrogeneous elements" called as "list"
        "[]"
        index starts from "0"
        mutable
"""

# list1 = [10,20,30,40,50]
# print(list1[0], list1[-5])
# print(list1[2],list1[-3])
# print(list1[0:3])
# print(list1[:2])
# print(list1[2:])
# print(list1[-3:-1])
# print(list1[::-1])
# print(list1[::-2])
# print(list1[::-3])
# list1[0] = 1000
# print(list1)

"""
    tuple
    *****
        collection of hetrogeneous elements
        index starts from 0
        ()
        immutable
        faster compared to list
        tuple takes less memory compared to list
"""

# import sys
# list1 = [10,20,30,40,50]
# tuple1 = (10,20,30,40,50)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(tuple1))

# tuple2 = (10,20,30,40,50)
# tuple2[0] = 1000
# print(tuple2[::-3])

# list1 = [10,"Hello",True]
# tuple1 = (10,"Gen AI", 10.1)
# print(type(list1),end=" | ")
# print(type(tuple1),end=" | ")

# dictionary
# key & value pairs
# {} / dict()
# keys are "immutable"
# values are "mutable"

# details = {
#     "name" : "Gen AI",
#     "ver" : 2
# }
# print(details)
# print(details["name"])
# details["name"] = "Agentic AI"
# print(details)
# print(type(details))

# details = {
#     "name" : "Hello",
#     "name" : "Welcome",
#     "name": {
#         "name" : "DS"
#     }
# }
# print(details)

# set
# wont allows duplicates
# {}
# s1 = {10,20,30,10,20,30}
# print(s1)
# print(type(s1))

# s2 = {}
# print(type(s2))

# s3 = set()
# print(type(s3))

# s4 = set([10,10,10])
# print(s4)

# s5 = set((10,10,10))
# print(s5)

# None
# x = None
# print(x)
# print(type(x))
# print(x == x)
# print(x == 0)