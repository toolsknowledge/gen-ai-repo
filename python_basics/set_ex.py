# set - wont allows duplicates
# {} / set()

# Example-1
# s1 = {10,20,30,10,20,30}
# print(s1)
# print(type(s1))

# Example-2
# s1 = {}
# print(type(s1))
# s2 = set()
# print(type(s2))

# Example-3
# s1 = {1,2,3,4}
# s1.add(5)
# print(s1)

# s1.remove(5)
# print(s1)
# s1.remove(5)
# s1.discard(5)

# for element in s1:
#     print(element,end=" ")

# Example-4
# s1 = {1,2,3}
# s2 = {3,4,5}
#s3 = s1 | s2
#s3 = s1.union(s2)
#print(s3)

#s3 = s1 & s2
#s3 = s1.intersection(s2)
#print(s3)

# s3=s1-s2
# print(s3)
# s3 = s2-s1
# print(s3)

# s3 = s1^s2
# print(s3)

# Example-5
# studnets = ["Ravi","Ravi","Samba","John"]
# print(set(studnets))

# s1 = frozenset({1,2,3})
# s1.add(4)

# s1 = {1,2,2,3}
# print(len(s1))
