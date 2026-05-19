# """
#     dictionary
#         key & value pairs
#         mutable
#         unordered (before 3.7) 
#         ordered(python 3.7+)
#         key --> unique
#         value --> any thing
# """

# d1 = {"num1":200, 
#       "num2":100}
# print(d1)

# d2 = dict(num1=200,num2=100)
# print(d2)

# d3 = dict([("num1",200),("num2",100)])
# print(d3)

# d4 = {}
# print(d4)
# print(type(d1))


# d1 = {
#     "name" : "AshokIT",
#     "course" : "gen ai",
#     "fee" : 20000
# }
# print(d1["name"])
# print(d1["course"])
# print(d1["fee"])
# print(d1["new_batch"])


# print(d1.get("name"))
# print(d1.get("course"))
# print(d1.get("fee"))
# print(d1.get("new_batch"))


# d1 = {"num1":200}
# d1["num2"] = 100
# d1["num1"] = 2000
# d1.update({"num3":3000,"num4":4000})
# print(d1)


# d1 = {
#     "num1" : 300,
#     "num2" : 200,
#     "num3" : 100
# }

#del d1["num1"]
#print(d1)

# print(d1.pop("num1"))

# d1.popitem()
# print(d1)

# d1.clear()
# print(d1)


# d1 = {
#     "num1" : 300,
#     "num2" : 200,
#     "num3" : 100
# }
# print(d1.keys())
# print(d1.values())
# print(d1.items())

# d1 = {
#     "num1" : 300,
#     "num2" : 200,
#     "num3" : 100
# }
# for k in d1:
#     print(k)

# for v in d1.values():
#     print(v)

# for k,v in d1.items():
#     print(k,v)


# print( {x:x*x for x in range(5)} )


# print( { x:x*x for x in range(5) if x%2 == 0} )

# d1 = {
#     "i1" : {"name":"Samba","sub":"AI"}
# }
# print(d1["i1"]["name"])
# print(d1.get("i1").get("name"))

# d1 = {
#     "num1" : 200
# }

# # shallow copy
# d2 = d1.copy()
# d2["num2"] = 100

# print(d1)
# print(d2)

# d1 = {
#     "num1" : 200
# }
# d2 = d1 # Reference Copy
# d2["num2"] = 100
# print(d1)

# allowed (int float string tuple boolean None)
# not allowed (list dict set)

# d1 = {
#     (1,2) : "Hello",            #tuple
#     # [1,2] : "Welcome"         #list
#     1 : "Hello_1",              #int
#     1.1:"Hello_2",              #float
#     "msg" : "Hello_3",          #string
#     # {"num1":200} : "Hello_4"  #dictionary
#     # {1} : "Hello_5",          #set
#     True : "Hello_6",           #boolean
#     None : "Hello_7"            #None
# }
# print(d1)

# str = "aabbcc"
# d1 = {}
# for ch in str:
#     d1[ch] = d1.get(ch,0)+1
# print(d1)









