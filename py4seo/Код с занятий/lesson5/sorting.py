from time import time


with open('buy.csv') as f1:
    f1.__next__()
    keys_buy = [x.split('\t')[0] for x in f1]

    # keys_buy = []
    # for line in f1:
    #     data = line.strip().split('\t')
    #     data = (data[0], int(data[1]), int(data[2]))
    #     keys_buy.append(data)

    print(keys_buy[:10])


t1 = time()

keys_buy.remove('buy')
keys_buy.sort(key=lambda x: x.split()[1], reverse=True)

t2 = time()


print('All done! Time is: ', round(t2-t1, 4))
print(keys_buy[:10])
