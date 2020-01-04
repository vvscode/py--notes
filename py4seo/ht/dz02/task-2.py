import re
import json
import pprint

words_splitter = re.compile("\W")


def get_words_count(value):
    return len(words_splitter.split(value))


def get_keyword_density(value, keyword):
    normalized_value = value.lower()
    normalized_keyword = keyword.lower()
    return normalized_value.count(normalized_keyword) / get_words_count(value)


def get_density_str(density):
    return f"{density*100:.2f}%"


def get_keyword_count(text, keyword):
    return text.lower().count(keyword.lower())


# Написать скрипт, в котором вручную задать 5 переменных url, title, description, h1, keyword.
# Внутрь этих переменных написать данные с какой-нибудь реальной html страницы.
url = "https://py4you.com/courses/python-for-seo/"
title = """Курс Python для SEO - Онлайн 
Интенсив 
48 часов занятий за 500 USD"""
description = """Python для SEO. Курс Python для SEO специалиста - это курс программирования с практическим уклоном на решение SEO задач. Курс включает&amp;nbsp;базовые и продвинутые ... """
h1 = "Python для SEO"
keyword = "курс"

# Затем нужно определить количество символов и количество слов в url, title, description, h1.
url_words_count = get_words_count(url)
title_words_count = get_words_count(title)
description_words_count = get_words_count(description)
h1_words_count = get_words_count(h1)

url_symbols_count = len(url)
title_symbols_count = len(title)
description_symbols_count = len(description)
h1_symbols_count = len(h1)

# Определить количество вхождений ключевого слова в title, description, h1.
title_keyword_count = get_keyword_count(title, keyword)
description_keyword_count = get_keyword_count(description, keyword)
h1_keyword_count = get_keyword_count(h1, keyword)

# Определить плотность ключевого слова в процентах в title, description, h1.
title_keyword_density = get_keyword_density(title, keyword)
description_keyword_density = get_keyword_density(description, keyword)
h1_keyword_density = get_keyword_density(h1, keyword)

# Всю информацию вывести в консоль в виде словаря в “красивом” виде.
stats_info = {
    "url": url,
    "Ключевое слово": keyword,
    "Заголовок страницы": {
        "Значение": title,
        "Число слов": title_words_count,
        "Число символов": title_symbols_count,
        "Число вхождения ключевого слова": title_keyword_count,
        "Процентная плотность ключевого слова": get_density_str(title_keyword_density),
    },
    "Описание": {
        "Значение": description,
        "Число слов": description_words_count,
        "Число символов": description_symbols_count,
        "Число вхождения ключевого слова": description_keyword_count,
        "Процентная плотность ключевого слова": get_density_str(
            description_keyword_density
        ),
    },
    "Заголовок первого уровня": {
        "Значение": h1,
        "Число слов": h1_words_count,
        "Число символов": h1_symbols_count,
        "Число вхождения ключевого слова": h1_keyword_count,
        "Процентная плотность ключевого слова": get_density_str(h1_keyword_density),
    },
}

print("json.dumps:")
print(json.dumps(stats_info, indent=2, ensure_ascii=False))

print("pprint:")
pprint.pprint(stats_info)
