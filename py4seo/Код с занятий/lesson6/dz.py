keyword = input('Введите запрос: ')
minus = input('Введите минус слова через запятую: ')

print(keyword)


def key_selection(keyword):
    results = list()
    with open('EnglishKeywords.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if any(mn in line for mn in minus.split(',')):
                continue
            print(line)
            if any(kw in set(line.split()) for kw in keyword.split(',')):
                print('i am in if')
                results.append(line.strip())

    with open(keyword + 'results.csv', 'w', encoding='utf-8') as f2:
        f2.write(f'Keywords;Words Count;Symbols Count\n')
        for key in results:
            print(key)
            words_count = len(key.split())
            print(words_count)
            symbols_count = len(key)
            print(symbols_count)
            raw = f'{key};{words_count};{symbols_count}\n'
            print(raw)
            f2.write(raw)


print('я тут')

key_selection(keyword)

print('я после вызова')
