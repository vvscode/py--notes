import csv

import pickle
import json

from time import time

key = input('Введите искомый ключ: ')

t1 = time()

result = list()


with open('about-aston-martin.info.txt', 'r', encoding='utf-8') as f:

    for line in f:
        line = line.strip()
        temp_list = line.split()

        if key in temp_list:

            words_count = len(line.split())
            symbols_count = len(line)

            raw = {
                'Keyword': line,
                'Symbols': symbols_count,
                'Words Count': words_count
            }

            result.append(raw)

            del words_count, symbols_count, raw

        del temp_list, line


t2 = time()

print(f'All Done! Found {len(result)} keywords')
print('Workung time is: ', round(t2 - t1, 4), 'seconds')

print(result)


with open('dump.pkl', 'wb') as f2:
    pickle.dump(result, f2)


with open('dump.json', 'w') as f3:
    json.dump(result, f3, indent=4)
