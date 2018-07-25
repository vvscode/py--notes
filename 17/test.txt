from sys import argv
from os.path import exists

script, from_file, to_file = argv

print(f"Copying form {from_file} to {to_file}")

with open(from_file) as f: indata = f.read()

print(f"The input file is {len(indata)} bytes long")

print(f"Does the output file exist? {exists(to_file)}")

input("Ready, hit return to continue, CTRL-C to abort")

out_file = open(to_file, 'w')
out_file.write(indata)

print("Alright, all done.")

out_file.close()