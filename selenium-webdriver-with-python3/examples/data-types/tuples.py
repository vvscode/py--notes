print("""
Tuple
Like list but they are immutable
It means you can't change them
""")

my_list = [1, 2, 3]
print(my_list) # [1, 2, 3]

my_list[0] = 0
print(my_list) # [0, 2, 3]

my_tuple = (1, 2, 3, 2, 2, 3)
print(my_tuple) # (1, 2, 3, 2, 2, 3)

print(my_tuple[0]) # 1

print(my_tuple[1:]) # (2, 3, 2, 2, 3)

print(my_tuple.index(2)) # 1

print(my_tuple.count(3)) # 2
