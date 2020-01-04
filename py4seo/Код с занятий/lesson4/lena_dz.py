from pprint import pprint
from requests_html import HTMLSession

# Делаем проверку на корректность ввода URL:
while True:
    url = input('Введите URL страницы:')
    if 'http' in url:
        print('URL принят.')
        break
    else:
        print('URL должен начинаться с http:// или https://...')


# Делаем проверку на корректность ввода keyword:
while True:
    keyword = input('Введите ключевое слово:')
    if len(keyword) > 2:
        print('Ключевое слово принято.')
        break
    else:
        print('Ключевик слишком короткий...')

# Парсим со страницы нужные данные:
with HTMLSession() as session:
    resp = session.get(url)

try:
    title = resp.html.xpath('//title')[0].text
except Exception as e:
    print(type(e), e)
    title = ''

try:
    description = resp.html.xpath('//meta[@name="description"]/@content')[10]
except Exception as e:
    print(type(e), e)
    description = ''

try:
    h1 = resp.html.xpath('//h1')[0].text
except Exception as e:
    print(type(e), e)
    h1 = ''

# Приводим все слова в нижний регистр, чтобы находить ключевик
title_lower = title.lower()
desc_lower = description.lower()
h1_lower = h1.lower()

# преобразовываем строки в списки, чтобы посчитать количество слов
l_title = title_lower.split()
l_desc = desc_lower.split()
l_h1 = h1_lower.split()

# Баллы за длину title
if (len(title) >= 30) and (len(title) <= 70):  # 10 баллов, если длина 30-70 символов
    tlenrate = 10
elif (len(title) > 70) and (len(title) <= 80):  # 5 баллов, если длина 71-80 символов
    tlenrate = 5
else:
    tlenrate = 0  # 0 баллов во всех других случаях

# Баллы за длину description
if (len(description) >= 100) and (len(title) <= 140):  # 5 баллов, если длина 100-140 симв, иначе 0 баллов
    dlenrate = 5
else:
    dlenrate = 0

# Баллы за наличие кея в title, description, h1
if keyword in title_lower:  # 25 баллов за кей в тайтле
    tkey = 25
else:
    tkey = 0

if keyword in desc_lower:  # 5 баллов за кей в description
    dkey = 5
else:
    dkey = 0

if keyword in h1_lower:  # 25 баллов за кей в h1
    hkey = 25
else:
    hkey = 0


tkeynum = 0
#  Баллы за отдаленность кея от начала строки
for number, word in enumerate(l_title, start=1):
    if keyword in word:
        if number <= 3:
            tkeynum = 15  # 15 баллов, если кей на 1 или 2 месте


hkeynum = 0
# Баллы за отдаленность кея от начала строки в H1
for h_number, h_word in enumerate(l_h1, start=1):
    if keyword in h_word:
        if h_number == 1:
            hkeynum = 15  # 15 баллов, если h1 начинается с кея


estimate = sum([tlenrate, dlenrate, tkey, dkey, hkey, tkeynum, hkeynum])

print()
print()
pprint('Title страницы:')
pprint(title)
print()
pprint('Description страницы:')
pprint(description)
print()
pprint('Заголовок h1:')
pprint(h1)
print()
print()
pprint('Считаем баллы:')
print()
pprint('Балл за длину Title:')
print(tlenrate)
print()
pprint('Балл за длину Description:')
print(dlenrate)
print()
pprint('Балл за наличие кея в Title:')
print(tkey)
print()
pprint('Балл за наличие кея в Description:')
print(dkey)
print()
pprint('Балл за наличие кея в h1:')
print(hkey)
print()
pprint('Балл за близость кея к началу Title:')
print(tkeynum)
print()
pprint('Балл за близость кея к началу h1:')
print(hkeynum)
print()
print()
pprint('ОБЩИЙ БАЛЛ:')
print(estimate)
