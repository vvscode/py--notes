list = ['a', 'b', 'c']
print(
    [i.capitalize() for i in list]
)

non_flat = [[1, 2], [3, 4], [5, 6, 7]]
print(
    [y for x in non_flat for y in x]
)

print(
    [x for x in range(10) if x % 2 == 0]
)
