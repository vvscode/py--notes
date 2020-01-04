from time import time


with open('buy.csv') as f1:
    f1.__next__()
    keys_buy = {x.split('\t')[0] for x in f1}


with open('essay.csv') as f2:
    f2.__next__()
    keys_essay = {x.split('\t')[0] for x in f2}


t1 = time()

results = keys_buy.union(keys_essay)

t2 = time()


print('All done! Time is: ', round(t2-t1, 4))
print('Results: ', len(results))
