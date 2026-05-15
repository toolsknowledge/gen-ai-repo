import numpy as np

# Example-12
# arr1 = np.array([10,50,20,40,30])
# print(np.sort(arr1)[::-1])


# Example-11
# arr1 = np.array([1,2,3,4,5])
# print(arr1[0])
# print(arr1[-5])
# print(arr1[1:3])
# print(arr1[-3:-1])
# print(arr1[1:])
# print(arr1[-2:])
# print(arr1[:2])


# Example-10
# arr1 = np.array([[10,20,30],
#                  [40,50,60]])
# print(np.sum(arr1,axis=0)) # col wise
# print(np.sum(arr1,axis=1)) # row wise


# Example-9 ( mean(), max(), min() )
# marks = np.array([60,90,70,80,75])
# np.mean(marks)


# Example-8
# print(np.random.rand(3))
# print(np.random.randint(100,200,5))


# Example-7
# arr1 = np.array([1,2,3,4,5,6])
# arr2 = arr1.reshape(2,3)
# print(arr2)
# arr3 = arr2.flatten()
# print(arr3)


# Example-6 (Predefined Functions)
# arr1 = np.array([1,2,3])
# arr2 = np.array([4,5,6])
# print( np.add(arr1,arr2) )
# print( np.subtract(arr1,arr2) )
# print( np.multiply(arr1,arr2) )
# print( np.divide(arr1,arr2) )
# print( np.pow(arr1,2) )
# print( np.mod([10,20,30],3) )
# print( np.remainder([10,20,30],3) )



# Example-5 (Braodcasting)
# num = 10
# arr1 = np.array([10,20,30])
# print(arr1 + num)
# arr2 = np.array([[10,20,30],[40,50,60]])
# print(arr2+num)


# Example-4
# arr1 = np.array([10])
# arr2 = np.array([10,20,30])
# print(arr1 + arr2)


# Example-3 (Vectorization)
# arr1 = np.array([1,2,3])                 
# arr2 = np.array([4,5,6])
# print(arr1 + arr2)
# print(arr1 - arr2)
# print(arr1 * arr2)
# print(arr1 / arr2)



# Example-2
# print( np.zeros((3,3)) )
# print( np.ones((2,2)) )
# print( np.eye(3) )
# print( np.arange(0,10,2) )
# print( np.linspace(0,1,5))
# print( np.full((2,2),10) )


# Example-1
# 1D Array
# arr1 = np.array([10,20,30,40,50])
# # 2D Array
# arr2 = np.array([[1,2],
#                  [3,4],
#                  [5,6]])
# print(arr1.shape)
# print(arr2.shape)
# print(arr1.dtype)
# print(arr2.dtype)
# print(arr1.ndim)
# print(arr2.ndim)


