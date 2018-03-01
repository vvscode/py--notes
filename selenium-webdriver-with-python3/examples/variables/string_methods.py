# certain symbol
print("some string"[0])

city = "Minsk"
# city[1] = "I" doesnt' supported
print(city)

print(len("some"))
print("Minsk".lower())
# print("some".len())
print("some".upper())
print("some" + str(2))


# replace
a = "1abc2abc3abc4abc"
print(a.replace('abc', 'ooo')) # replace all
print(a.replace('abc', 'ooo', 2)) # replace only two

# substrings
# starting inclusive
# ending exclusive
a = "some string"
print(a[1:6]) # sOME String
print(a[5:])
print(a[::-1]) # reverse
print(a[0::2]) # a[0, len(a): 2]