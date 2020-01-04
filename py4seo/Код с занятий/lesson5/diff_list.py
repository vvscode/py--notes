from time import time


with open('buy.csv') as f1:
    f1.__next__()
    keys_buy = [x.split('\t')[0] for x in f1]


with open('essay.csv') as f2:
    f2.__next__()
    keys_essay = [x.split('\t')[0] for x in f2][:10000]


t1 = time()

results = list()

for k in keys_buy:
    if k in keys_essay:
        results.append(k)

t2 = time()


print('All done! Time is: ', round(t2-t1, 4))
print('Results: ', len(results))
