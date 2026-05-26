# set - "datatype"
# wont "allows duplicates"
# "unordered"
# "mutable"
# fast searching
# {} / set()

# s1 = {10,20,30,10,20,30}
# print(s1)
# print(type(s1))

# s1 = {}
# print(type(s1))
# s2 = set()
# print(type(s2))

# s1 = {1,2,3}
# s1.add(4)
# print(s1)
# s1.update([5,6,7])
# print(s1)

# s1.remove(3)
# print(s1)

# s1.remove(3)
# s1.discard(3)

# s1.pop()
# print(s1)

# s1.clear()
# print(s1)


# s1 = {1,2,3}
# s2 = {3,4,5}
# print(s1 | s2)        # {1,2,3,4,5}
# print(s1.union(s2))

# print(s1 & s2)  # {3}
# print(s1.intersection(s2))

# print(s1 - s2) # {1,2}
# print(s2 - s1)

# print(s1^s2)

# s1 = {10,20,30,40,50}
# print(30 in s1)
# print(10 not in s1)

# for element in s1:
#     print(element)

# print({x*x for x in range(1,6)})

# s1 = frozenset([1,2,3])
# s1.add(4)

# emails = ["test@gmail.com","test1@gmail.com","test@gmail.com"]
# print(set(emails))

# s1 = {"std1","std2","std3"}
# s2 = {"std1","std4","std5"}
# print(s1 & s2)