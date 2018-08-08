i = 0
numbers = []

while i < 6:
    print("At the top i is {}".format(i))
    numbers.append(i)

    i = i + 1
    print("Numbers now: ", numbers)
    print("At the bottom i is {}".format(i))

print("The numbers:")

for num in numbers:
    print(num)

print('#############')


def createNumbers(max, step):
    i = 0
    numbers = []
    for i in range(0, max, step):
        print("At the top i is %d" % i)
        numbers.append(i)

        print("Numbers now: ", numbers)
        print("At the bottom i is %d" % i)
    return numbers


numbers = createNumbers(10, 2)

print("The number: ")

for num in numbers:
    print(num)
