# set - unique elements(wont allows duplicates), unordered collection, mutable (condition : element must be immutable)

# unordered.   no index
# Unique 
# mutable
# can't access through indexes
# Fast O(1) lookup



# s1 = {1,2,3,4,5}
# print(len(s1))


# s1 = set("hello")
# print(s1)

# print( {1,2,3} == {3,2,1} )



# s1 = {1,2,3}
# s1.add((4,5))
# print(s1)



# list1 = [1,2,3]
# list2 = [2,3,4]
# print(set(list1) & set(list2))


# s1 = frozenset([1,2,3])
# s1.add(4)

# list1 = ["java","java"]
# s1 = set(list1)
# print(s1)

# s1 = {"ml","dl","nlp","gen ai","agentic ai","ml"}
# print(s1)


# s1 = {x*x for x in range(5)}
# print(s1)



# s1 = {1,2,3}
# print(2 in s1)
# print(5 in s1)





# s1 = {1,2}
# s2 = {1,2,3}
# print(s1.issubset(s2))
# print(s2.issuperset(s1))




# s1 = {1,2,3}
# s2 = {3,4,5}
# print(s1 | s2)
# print(s1.union(s2))

# print(s1 & s2)
# print(s1.intersection(s2))

# print(s2-s1)
# print(s1 ^ s2) # remove common keep unique



# s1 = {1,2,3}
# s1.remove(2)
# print(s1)
# s1.discard(4)
# print(s1)
# x = s1.pop()
# print(x)
# print(s1)
# s1.clear()
# print(s1)


# s1 = {1,2}
# s1.add(3)
# s1.update([4,5])
# print(s1)


# s1 = {1,2,3}
# s2 = set([1,2,3])
# s3 = set()
# print(s1)
# print(s2)
# print(s3)