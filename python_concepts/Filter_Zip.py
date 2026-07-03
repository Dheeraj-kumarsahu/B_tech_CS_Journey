nums =[1,2,3,4,5]

#map-transform each element in the list
doubled=list(map(lambda x :x * 2,nums))

#filter-keep items that satisfy a condition
evens=list(filter(lambda x :x %2==0,nums))

print(f'Mapping-transform each element in the list :- {doubled}')
print(f'Filter-keep items that satisfy a condition  :- {evens}')