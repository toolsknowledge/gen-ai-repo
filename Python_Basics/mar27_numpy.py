import numpy as np


list1 = np.array([1,2,3,4,5])

print(list1.reshape(1,-1))





#mar-28
# list32 = np.array([[1,2],
#                    [3,4]])
# list33 = np.array([[5,6],
#                    [7,8]])
# #print(np.dot(list32,list33))
# print(list32.T)




# list31 = np.array([1,3,2])
# print(np.sort(list31))
# print(np.argsort(list31))




# print( np.random.rand(2,2) ) # <1
# np.random.seed(0)
# print( np.random.randint(1,10,(2,3)))
# np.random.seed(0)
# print( np.random.rand(2,2) )



# list29 = np.array([1,2,3])
# list30 = list29.copy() # copies
# list30[0] = 100
# print(list29) #[1 2 3]


# list27 = np.array([1,2,3])
# list28 = list27 # reference copy
# list27[0] = 100
# print(list28) #[100   2   3]




# list26 = np.array([1,2,3,4,5,6])
# new_list = np.split(list26,2)
# print(new_list[0])
# print(new_list[1])

# list24 = np.array([1,2])
# list25 = np.array([3,4])
# print(np.vstack((list24,list25)))
# print(np.hstack((list24,list25)))



# list23 = np.arange(6)
# print(list23)
# print(list23.reshape(2,3))
# print(list23.flatten())



# list22 = np.array([[1,2,3],
#                    [4,5,6],
#                    [7,8,9]])
# print(np.sum(list22,axis=0)) # col wise sum
# print(np.sum(list22,axis=1)) # row wise sum



# list21 = np.array([1,2,13,41])
# print(np.sum(list21))
# print(np.mean(list21))
# print(np.max(list21))
# print(np.min(list21))
# print(np.std(list21))             #low std --> data is consistent  high std --> data not consistant





# list20 = np.array([1,4,9])
# print(np.sqrt(list20))
# print(np.exp(list20))   
# print(np.log(list20))     
# print(np.sin(list20))




# list19 = np.array([[10,20,30],
#                    [40,50,60],
#                    [70,80,90]])
# for inner_list in list19:
#     print("-------")
#     for element in inner_list:
#         print(element)
       




# list18 = [10,20,30,40,50]
# for element in list18:
#     print(element)






# list16 = np.array([1,2,3])
# list17 = np.array([4,5,6])
# print( list16 + list17 )
# print( list16 * list17 )
# print( list16 ** 2 )
# print( list17 ** 2 )



# list15 = np.array([10,20,30,40,50])
# new_list = list15[list15>20]
# print(new_list)
# print(list15)


# list14 = np.array([[1,2,3,4,5],
#                    [6,7,8,9,10],
#                    [11,12,13,14,15],
#                    [16,17,18,19,20]])
#print(list14[0,:])     row0
#print(list14[0:2,:])   row0 & row1
#print(list14[:,0])     col0
#print(list14[:,0:3])   col0,col1,col2


# list13 = np.array([[1,2,3],[4,5,6],[7,8,9]])
# print(list13)
# print(list13[0,:])          # row 1
# print(list13[0:2,:])        # row0 & row1
# print(list13[:,0])          # col0
# print(list13[:,0:2])        # 0col & 1col



# list12 = np.array([[1,2,3],
#                   [4,5,6]])
# print( list12[0,0] ) # 0 row 0 col --> 1
# print( list12[1,2] ) # 1 row 2 col --> 6
# print( list12[:,0] ) # 0 col [1,4]
# print( list12[:,1] ) # 1 col [2,5]
# print( list12[:,2] ) # 2 col [3,6]
# print( list12[0,:] ) # 0 row [1,2,3]
# print( list12[1,:] ) # 1 row [4,5,6]



# list11 = np.array([10,20,30,40,50])
# print(list11[2],list11[-3])
# print(list11[0:3])
# print(list11[1:4])
# print(list11[2:])
# print(list11[:2])
# print(list11[-3:])
# print(list11[-3:-1])


# list10 = np.array([[1,2,3],[4,5,6]],dtype=float)
# print(list10.shape)
# print(list10.ndim)
# print(list10.size)
# print(list10.dtype)



# list9 = np.linspace(0,3,4)
# print(list9)

# list8 = np.full((2,2),7)
# print(list8)

# list7 = np.arange(1,10,2)
# print(list7)

# list6 = np.eye(3)
# print(list6)

# list5 = np.ones((3,3))
# print(list5)

# list4 = np.zeros((3,3))
# print(list4)

# list1 = np.array([10,20,30,40,50])
# print(list1)
# print(list1.shape)

# list2 = np.array([[1,2],[3,4],[5,6]])
# print(list2)
# print(list2.shape)

# list3 = np.array([10,20,30],dtype=float)
# print(list3)