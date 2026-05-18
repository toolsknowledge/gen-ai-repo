# dict - key & value
# mutable
# Unordered (<3.7), ordered(3.7+)

# d1 = {"num1":200, "num2":100}
# print(d1)

# d2 = dict(num1=200, num2=100)
# print(d2)

# d3 = dict([("num1",200),("num2",100)])
# print(d3)

# d4 = {}
# print(d4)


d1 = {"num1":100,"num2":200}
# access
# print(d1["num3"])
# print(d1.get("num3"))

# adding element & update element
# d1["num3"] = 300
# d1["num1"] = 1000
# d1.update({"num2":2000,"num3":3000})
# print(d1)

# delete
# del d1["num1"]
# print(d1)

# print(d1.pop("num3"))

# d1.popitem()
# print(d1)

# d1.clear()
# print(d1)

# for k in d1:
#     print(k)
# for v in d1.values():
#     print(v)
# for k,v in d1.items():
#     print(k,v)

# print(d1.keys())
# print(d1.values())
# print(d1.items())


# d1 = {x:x*x for x in range(5) if x%2 == 0}
# print(d1)


# students = {
#     "s1" : {"name":"Std1","marks":90},
#     "s2" : {"name":"Std2","marks":80}
# }
# print(students["s1"]["marks"])

# d1 = {
#     "num1" : 100
# }
# # d2 = d1.copy() # shallow copy
# d2 = d1          # ref copy
# d1["num1"] = 1000
# print(d1)
# print(d2)

# keys (int, float, string, tuple) (allowed)
# list, dict (not allowed)
# d1 = {
#     10 : "Hello",
#     10.1 : "Welcome",
#     10.1 : "Bye",
#     "str1" : "Python" ,
#     (1,2) : "Dict",
#     True:"Hi",
#     None:"Helo",
#     [10,20]:"Hello"
# } 
# print(d1)

# str = "aabbcc"
# freq = {}
# for ch in str:
#     freq[ch] = freq.get(ch,0) + 1

# print(freq)

# d1 = {"a":3,"c":2,"b":1}
# print( sorted(d1.items(),key=lambda x:x[0]) )