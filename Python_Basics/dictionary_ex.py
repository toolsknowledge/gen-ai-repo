"""
    key & value pairs
    keys are immutable
    values are mutable
"""
# d1 = {
#     "key1" : 100,
#     "key2" : 200,
#     "key3" : 300
# }
# print(d1)

d1 = dict(key1=100,key2=200,key3=300)

# print(d1["key1"])
# print(d1["key4"]) # Err

# print(d1.get("key1"))
# print(d1.get("key4"))

d1.pop("key1")
print(d1)

d1.popitem()
print(d1)

d1.clear()
print(d1)