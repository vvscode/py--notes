print('*'*50)
print('Сейчас мы выгрузим из Базы букварикс все слова, которые Вам нужны!')
my_keys = input('Введите ключевые слова через запятую: ')
my_keys = [k.strip() for k in my_keys.split(',')]

print('*'*50)
print('OR операция - слова где встречается хотя бы одно из указанных вами')
print('AND операция - слова где встречаются все из указанных вами')
variant = input('Ищем слова как or или and операцию? Введите or или and: ')
variant = variant.strip().lower()
assert variant in ['or', 'and'], 'Можно ввести только OR или AND'
print('*'*50)
print('Процесс поиска запущен. Подождите, это займет какое-то время...')

bukvarix_file = open('EnglishKeywords.txt', 'r', encoding='utf-8')
my_keys_file = open('my_keys.txt', 'w', encoding='utf-8')


for line in bukvarix_file:
    if variant == 'or':
        if any([k in line for k in my_keys]):
            my_keys_file.write(line)
    elif variant == 'and':
        if all([k in line for k in my_keys]):
            my_keys_file.write(line)

print('Готово!')
print('*'*50)
