list = ['a', 'b', 'c']
gen = (i.capitalize() for i in list)

print(next(gen))
print(next(gen))
print(next(gen))
# print(next(gen)) #StopIteration

# for i in gen:
#     print(i)


def do_thing():
    yield 'a'
    yield 'b'
    yield 'c'


for x in do_thing():
    print("value: {}".format(x))
