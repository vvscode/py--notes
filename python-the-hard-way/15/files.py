from sys import argv

script, filename = argv

txt = open(filename)

print(f"Here's file `{filename}` content")
print(txt.read())