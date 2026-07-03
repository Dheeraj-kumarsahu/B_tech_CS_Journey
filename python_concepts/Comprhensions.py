# list Comprehension
a=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
b=[i for i in a if i % 2 ==  0]
print(b)

cubes_dict={x:x**3 for x in b}
print(cubes_dict)

unique={x%3 for x in range(10)}
print(unique)