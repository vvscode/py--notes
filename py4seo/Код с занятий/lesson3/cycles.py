keywords = '''
купить ноутбук дешево
купить ноутбук игровой
купить ноутбук эльдорадо
ноутбук купить украина
ноутбуки ціни
купить ноутбук асус
ноутбуки фокстрот
ноутбук алло
'''.strip().split('\n')


print(keywords)


word = 'ціни'

# if word in keywords[0]:
#     print('в первое слово входит цена')
#
# if word in keywords[1]:
#     print('во второе слово входит цена')


keyword = 'buy essays online'


# keywords = set(keywords)

for i, keyword in enumerate(keywords, start=1):

    for k in range(100):
        if k > 90:
            print(k)
            break

    if 'эльдорадо' in keyword:
        continue

    print('Ключ: ', keyword)
    if word in keyword:
        print('Цена входит в ключ: ', keyword, i)


dict_vhojd = {
    'количество символов в URL': 134,
    'количество символов в title': 75,
    'количество символов в description': 165,
    'количество символов в h1': 28,
    'количество символов в keyword': 13,
    'количество слов в URL': 4,
    'количество слов в title': 9,
    'количество слов в description': 25,
    'количество слов в h1 ': 3,
    'вхождения в title': 4.5,
    'вхождения в h1': 25.0,
    'вхождения в description': 14.0,
}


# for key, value in dict_vhojd.items():
#     print('Ключ', key)
#     print('Значение', value)


print('All done!')


print(keyword)
