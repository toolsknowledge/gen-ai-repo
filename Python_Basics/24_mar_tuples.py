# tuple
# ordered
# immutable collection (can't change)
# allows duplicates
# ()


t1 = (10,[20,30],40)
t1[1] = [200,300]



# t1 = (10,)
# print(type(t1))


# t1 = "hello","welcome"
# print("*".join(t1))

# t1 = (3,1,2)
# print( tuple(sorted(t1)) )


# stds = ("Std1","Std2")
# marks = (90,95)
# pairs = list(zip(stds,marks))
# print(pairs)
# x,y = zip(*pairs)
# print(x)
# print(y)

# a = 10
# b = 20
# b,a=a,b
# print(b,a)



# def test():
#     return 1,2,3
# t1 = test()
# e1,e2,e3 = t1
# print(e1,e2,e3)




# t1 = ((1,2),(3,4),(5,6))
# for o in t1:
#     for i in o:
#         print(i)

# t1 = (1,2)
# t2 = (3,4)
# t3 = t1 + t2
# print(t3)
# t4 = t3 * 3
# print(t4)

# t1 = (10,20,30,40,50)
# print(len(t1))
# print(max(t1))
# print(min(t1))
# print(sum(t1))




# t1 = (1,2,3,4,5)
# print(3 in t1)
# print(100 in t1)

# t1 = (1,2,1,2,3)
# print(t1.count(2))
# print(t1.count(1))
# print(t1.count(3))
# print(t1.index(1))
# print(t1.index(3))



# t1 = (10,20,30)
# list1 = list(t1)
# list1.append(40)
# t2 = tuple(list1)
# print(t2)


# t1 = (10,[20,30],40)
# t1[1][0] = 200
# print(t1)


# t1 = 10,20,30
# t1[0] = 1000 # Err



# t1 = 10,20,30
# e1, e2, e3 = t1
# print(e1, e2, e3)
# x, *y = t1
# print(x)
# print(y)
# print(type(y))





# t1 = (10,20,30,40,50)
# print(t1[0])
# print(t1[-1])
# print(t1[1:4])
# print(t1[:4])
# print(t1[1:])
# print(t1[::-1])
# for ele in t1:
#     print(ele)





# t1 = (10,20,30)
# print(t1)
# print(type(t1))
# t2 = (10,)
# print(t2)
# t3 = 100,200,300
# print(t3)