

def ip_gen():
    for i_1 in range(256):
        for i_2 in range(256):
            for i_3 in range(256):
                for i_4 in range(256):
                    yield f"{i_1}.{i_2}.{i_3}.{i_4}"


gen_1 = (f'bla bla {i}' for i in range(1000000))

gen_2 = ip_gen()


for _ in range(100):
    ip = gen_2.__next__()
    print(ip)


print(gen_1)
print(gen_2)
