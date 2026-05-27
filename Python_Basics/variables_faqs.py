"""
    "==" (compares values) (wont compare memory / objects)
    "is" compares objects/memory

    num,float,bool,str,tuple,None -- both are true
    list, dict,set -- True / False
"""

flag = ""
if flag:
    print("Hello")
else:
    print("Gen AI")

res = "Hello" if flag else "Gen AI"
print(res)

# x = "10"
# y = 5
# print(x * y)
# print(int(x) + y)
# print(int(x) / y)
# print(int(x) * y)


# / (division)
# // (floor division)

# print(10/3) #3.3333333333333335
# print(10 // 3) #3
# print(10 % 3) #Reminder 1





# deep copy
# x = 100
# y = x
# print(y) #100

# x = 200
# print(y) #100



# str = "Hello"
# print(str[0])
# print(str[-5:-3])

# num1 = 0x1010ABC
# print(num1) #16845500

# num2 = 0o123
# print(num2) #83

# num3 = 0b1010
# print(num3) #10


# x = 10
# y = 10
# print(x==y)
# print(x is y)

# x1 = 10.1
# y1 = 10.1
# print(x1 == y1)
# print(x1 is y1)

# x2 = True
# y2 = True
# print(x2 == y2)
# print(x2 is y2)

# x3 = "Hello"
# y3 = "Hello"
# print(x3 == y3)
# print(x3 is y3)

# x4 = [10,20]
# y4 = [10,20]
# print(x4 == y4)
# print(x4 is y4)

# x5 = (10,20)
# y5 = (10,20)
# print(x5 == y5)
# print(x5 is y5) # True

# x6 = {"name":"Gen AI"}
# y6 = {"name":"Gen AI"}
# print(x6 == y6)
# print(x6 is y6)

# x7 = {1,2}
# y7 = {1,2}
# print(x7 == y7)
# print(x7 is y7)

# x8 = None
# y8 = None
# print(x8 == y8)
# print(x8 is y8)


"""
    Falsy
        0, 0.0, "", [], {}, set(), None, False,.....
    Truthy
        1 10.1 "Hello" [1,2] {name:"Samba"},....
    
"""
# print(bool(0),end=" ")
# print(bool({}),end=" ")
# print(bool(False),end=" ")

# print(bool(1),end=" ")
# print(bool(-10),end=" ")
# print(bool("False"),end=" ")



