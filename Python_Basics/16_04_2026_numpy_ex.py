import numpy as np

# Example-1
# list1 = np.array([10,20,30,40,50])
# print(list1)
# print(list1.shape) #(5,)
# print(list1.ndim)  #1
# print(list1.dtype) #int64

# list2 = np.array([[1,2,3],
#                   [4,5,6],
#                   [7,8,9]])
# print(list2.shape) #(3, 3)
# print(list2.ndim)  #2
# print(list2.dtype) #int64

# Example-2
# print( np.zeros((2,3)) )
# print( np.ones((2,3)) )
# print( np.eye(3) )
# print( np.arange(0,10,2) )
# print( np.linspace(0,1,5) )

# Example-3
# list1 = np.array([10,20,30,40,50])
# print(list1[0]) #10
# print(list1[-5]) #10
# print(list1[1:3]) #1 will include and 3 will execlude [20,30] 
# print(list1[1:])  #1 to end [20,30,40,50]
# print(list1[:3])  # 0 will include and 3 will exclude [10,20,30]

# Example-4
# list1 = np.array([[1,2,3],
#                   [4,5,6]])
# print( list1[0][0] ) #1
# print(list1[1][2] )  #6
# print(list1[:,0]) # col1
# print(list1[:,1]) # col2
# print(list1[:,2]) # col3

# print(list1[0]) # row1
# print(list1[1]) # row2

# Example-5
# list1 = np.array([[1,2,3],
#                    [4,5,6],
#                    [7,8,9]])
# print(list1[:,0])
# print(list1[:,0:2])
# print(list1[0:2])

# Example-6
# Vectorization
# list1 = np.array([1,2,3])
# print(list1 + 2)
# print(list1 - 2)
# print(list1 * 2)
# print(list1 / 2)
# print(list1 ** 2)

# Example-7
# list1 = np.array([1,2,3,4,5])
# print(f'min element {np.min(list1)}')
# print(f'max element {np.max(list1)}')
# print(f'sum of element {np.sum(list1)}')
# print(f'mean of elements {np.mean(list1)}')
# print(f'square of element {np.sqrt(list1)}')

# Example-8
# list1 = np.array([1,2,3])
# list2 = np.array([[10],[11],[12]])
# print(list1 + list2)

# Example-9
# list1 = np.array([[1,2],
#                   [3,4]])
# list2 = np.array([[5,6],
#                   [7,8]])
# print(np.dot(list1,list2))


# Example - 10
# 0 10 100 42 # Mathematics (Number System Vendor)
# np.random.seed(42)
# print( np.random.rand(2,2) )
# print( np.random.randint(1,10,(2,3)) )
# print( np.random.rand(3) )


# print( np.full((3,3),100) )

# list1 = np.array([10,20,30,40,50])
# print(list1[list1>30])
# print(list1[list1<30])

# list1 = np.array( [[1,2,3],
#                     [4,5,6]] )
# print( np.sum(list1,axis=0) ) # column-wise sum
# print( np.sum(list1,axis=1) ) # row-wise sum

# list1 = np.arange(6)
# list2 = list1.reshape(2,3) # convert 1D - MD
# list3 = list2.flatten() # convert MD - ID
# print(list3)

# list1 = np.array( [1,2] )
# print(list1.reshape(-1,1)) # [[1],[2]]


# list1 = np.array([1,2])
# list2 = np.array([3,4])
# print( np.vstack( (list1,list2) ) )
# print( np.hstack( (list1,list2) ) )

# list1 = np.array([1,2,3,4,5,6,7,8,9])
# new_list = np.split(list1,3) 
# print(new_list[0])


# list1 = np.array([1,2,3])
# list2 = list1    # ref copy
# list1[0] = 1000
# print(list1)
# print(list2)

# list1 = np.array([1,2,3])
# list2 = list1.copy() # copy
# list1[0] = 1000
# print(list1)
# print(list2)

# list1 = np.array([3,1,2])
# print(np.sort(list1))
# print(np.argsort(list1))

# list1 = np.array([[1,2],
#                   [3,4]])
# list2 = np.array([[5,6],
#                   [7,8]])
# new_list1 = np.dot(list1,list2)
# print(new_list1)
# print(new_list1.T)



