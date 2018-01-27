numbers = [1, 2, 3]
for i in numbers:
    print(i)

sentence = 'some phrase'
for i in sentence:
    print(i)

letters = ['a', 'b', 'c']
print(zip(numbers, letters))
for l, n in zip(letters, numbers):
    print("{}: {}".format(l, n))

for i, n in enumerate(numbers):
    print("{} is #{} in list".format(n, i))
