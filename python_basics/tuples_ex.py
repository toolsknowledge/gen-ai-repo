# tuples
# collection of "ordered and hetrogeneous" elements called as tuple
# immutable
# ()
# charactristics: 1) ordered 2) immutable 3) allows duplicates. 4) hetrogenous elements. 5) faster. 7) indexed

# t1 = (1,2,3)
# print(t1)

# t1 = ()
# print(t1)
# print(type(t1))

# t2 = (10,)
# print(type(t2))

# t3 = (100)
# print(type(t3))

# t4 = (100,200,300,400,500)
# print(t4[0], t4[-5])
# print(t4[0:3])
# print(t4[:2])
# print(t4[2:])
# print(t4[::-1])
# print(t4[-3:-1])

# t5 = (10,20,30)
# e1,e2,e3 = t5
# print(e1,e2,e3)

# e1,*e2 = t5
# print(e2)
# print(e1)

# t6 = (100,200,300)
# t6[0] = 1000

# t7 = ('ML','DL','NLP','GenAI','AgenticAI')
# for element in t7:
#     print(element,end=" | ")

# t8 = ((10,20),(30,40),(50,60),(70,80),(90,100))
# e1,e2,e3,e4,e5 = t8

# x5,y5 = e5
# print(x5,y5)

# t9 = (10,20,30,10,20,30)
# print(t9.count(10))
# print(t9.count(20))
# print(t9.count(30))
# print(t9.index(10))
# print(t9.index(30))

# t1 = (10,20,30)
# t2 = (40,50,60)
# t3 = t1 + t2
# print(t3)
# print(t3 * 2)
# print(20 in t3)
# print(200 not in t3)

# t1 = (100,200,300)
# i = 0
# while i < len(t1):
#     print(t1[i])
#     i += 1


# t1 = (10,20,30,40,50)
# print(min(t1))
# print(max(t1))
# print(len(t1))
# print(sum(t1))

# t1 = (10,20,30)
# list() - converts tuple to list
# l1 = list(t1)
# l1[0] = 1000
# tuple() - converts list to tuple
# t2 = tuple(l1)
# print(t2)

# t1 = ([1,2],[3,4])
# t1[0].append(3)
# print(t1)

# import sys
# list1 = [10,20,30]
# tuple1 = (10,20,30)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(tuple1))

# def calc(num1,num2):
#     return num1+num2, num1-num2, num1*num2, num1/num2

# res = calc(200,100)
# add,sub,mul,div = res
# print(add,end=" ")
# print(sub,end=" ")
# print(mul,end=" ")
# print(div,end=" ")

students = (
    (101,"Std1","Java"),
    (102,"Std2","Python"),
    (103,"Std3","UI")
)
for sid,sname,sub in students:
    print(f"{sid} - {sname} - {sub}")

