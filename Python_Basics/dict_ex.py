"""
   dictionary
   **********
        key - value pairs
        keys are immutable
        values are mutable
        {}
"""
# d1 = {}
# print(type(d1))

# d2 = {
#     "name" : "Samba",
#     "sub" : "Gen AI"
# }
# print(d2)

# d1 = {
#     "key1" : "Hello",
#     "key2" : "Welcome"
# }
# print(d1["key1"])
# print(d1["key3"]) # Err

# print(d1.get("key1"))
# print(d1.get("key3"))


# d1 = {
#     "name" : "Hello"
# }
# d2 = dict([("name","Hello")])
# d3 = dict(name="Hello")
# print(d1)
# print(d2)
# print(d3)

# d1 = {
#     "key1" : 100,
#     "key1" : 1000
# }
# print(d1["key1"])

# d1 = {}
# d1["key1"] = 1000
# print(d1)

# d1 = {
#     "key1" : 100
# }
# d1["key1"] = 10000
# print(d1)


# d1 = {
#     "key1" : 100,
#     "key2" : 100
# }
# print(d1)

# d1 = dict(key1=100,key2=200)
# print(d1.keys())
# print(d1.values())
# print(d1.items())

# d1 = {
#     "key1" : 100,
#     "key2" : 200
# }
# for x in d1:
#     print(x)
# for y in d1.values():
#     print(y)
# for k,v in d1.items():
#     print(k,v)

# d1 = dict([("key1",100),("key2",200)])
# d1.pop("key1") # Deleted
# d1.pop("key1") # Err
# print(d1)

# d1 = dict(key1=100,key2=200)
# d1.popitem()
# print(d1)
# d1.clear()
# print(d1)

# d1 = dict()

# d1["key1"] = 100
# d1["key1"] = 1000
# d1["key2"] = 2000
# d1["key3"] = 3000

# d1.pop("key1")
# d1.popitem()
# d1.clear()
# print(d1)


# d1 = {
#     "key1" : [10,20,30,40,50],
#     "key2" : (10,20,30,40,50),
#     "key3" : {
#         "num1" : 100,
#         "num2" : 200
#     }
# }

# read key1
# read key2
# read key3

# print({x:x*x for x in range(5)})
# store cube of a number in the form of a dictonary

# d1 = {}
# list1 = []

# for x in range(5):
#     d1[x] = x*x
#     list1.append(x)

# print(d1)
# print(list1)

# copy() - shallow
# deepcopy() - deepcopy
# d1 = {
#     "key1" : [10,20]
# }

# keys must be hashable
# int, float, bool, str, bytes,tuple,fronzenset,NoneType (supports)
# list,dict,set,bytearray (wont)

# d1 = {
#     100: "Hello",
#     10.1 : "Welcome",
#     True : 100,
#     "Hello":200,
#     b'123' : 300,
#     (10,20,30) : 10,
#     frozenset() : 100,
#     None : 200
# }
# print(d1)

# d1 = {
#     # [1,2] : 100
#     # {} : "Hello",
#     # set() : 100
#     # bytearray(b'123') : 100
# }
# print(d1)





