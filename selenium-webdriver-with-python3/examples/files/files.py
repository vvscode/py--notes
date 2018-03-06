"""
File I/O
'w' -> Write-Only Mode
'r' -> Read-only Mode
'r+' -> Read And Write Mode
'a' -> Append Mode
"""

list = [1, 2, 3]

file = open("firstfile.txt", "w")

for item in list:
    file.write(str(item) + "\n")

file.close()

"""
File I/O
Reading a file -> .read()
Reading line by line -> .readline()
"""

file_to_read = open("firstfile.txt", 'r')

print(str(file_to_read.read()))
file_to_read.close()

print("Line by line ========>>")
file_line = open("firstfile.txt", 'r')
print(str(file_line.readline()), end='')
print(str(file_line.readline()), end='')
print(str(file_line.readline()))

file_line.close()

"""
With / As Keywords
"""
# print("Normal Write Start")
# my_write = open("textfile.txt", "w")
# my_write.write("Trying to write to the file")
# my_write.close()
#
#
# print("Normal Read Start")
# my_read = open("textfile.txt", "r")
# print(str(my_read.read()))

print("With As Write Start")
with open("withas.txt", "w") as with_as_write:
    with_as_write.write("This is an example of with as write/read")

print()
print("With As Read Start")
with open("withas.txt", "r") as with_as_read:
    print(str(with_as_read.read()))
