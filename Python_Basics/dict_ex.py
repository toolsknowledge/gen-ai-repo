# dictionary - key & value pairs
# {}, dict()
# keys are "immutable" and values are "mutable"

# d1 = {
#     "name" : "samba",
#     "age" : 40
# }
# print(d1)

# d2 = dict({"name" : "samba","age" : 40})
# print(d2)

# d1 = {
#     "name" : "samba",
#     "age" : 40
# }

# print(d1["name1"])
# print(d1.get("name1"))

# d1.pop("name1")
# print(d1)

# del d1["name1"]
# print(d1)

# d1.popitem()
# print(d1)

# d1.clear()
# print(d1)

# d1 = {}
# d1["name"] = "Samba"
# d1["age"] = 40
# print(d1)

# d1["age"] = 35
# print(d1)

# d1 = {
#     "name" : "samba",
#     "age" : 40
# }
# print(d1.keys())
# print(d1.values())
# print(d1.items())

# d1 = {
#     "name" : "samba",
#     "age" : 40
# }
# for key in d1:
#     print(key)
# for value in d1.values():
#     print(value)
# for key,value in d1.items():
#     print(key,value)

# print({x:x*x for x in range(1,6)})

# d1 = {"a":10,"b":20}
# print(len(d1))
# print(min(d1))
# print(max(d1))
# print("a" in d1)
# print("a" not in d1)

# d1 = {
#     (10,20) : [10,20]
# }


import copy
# shallow copy
# d1={"a":[1,2]}
# d2=copy.copy(d1)
# d1["a"].append(3)
# print(d2)

# deep copy
# d1={"a":[1,2]}
# d2=copy.deepcopy(d1)
# d1["a"].append(3)
# print(d2)
# print(d1)