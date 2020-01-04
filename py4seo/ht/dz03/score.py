import re
import json
import pprint
import argparse
from requests_html import HTMLSession
from collections import Counter

words_splitter = re.compile("\W")


def calculate_score(keyword, title="", description="", h1=""):
    lkeyword = keyword.lower()
    ltitle = title.lower()
    ldescription = description.lower()
    lh1 = h1.lower()

    title_keyword_count = ltitle.count(lkeyword)
    description_keyword_count = ldescription.count(lkeyword)
    h1_keyword_count = lh1.count(lkeyword)

    title_keyword_position = ltitle.find(lkeyword)
    h1_keyword_position = lh1.find(lkeyword)

    title_score = 35
    if title_keyword_count > 0 and title_keyword_count < 3:
        title_score *= 1
    elif title_keyword_count > 2:
        title_score *= 0.5
    else:
        title_score *= 0

    if title_keyword_position > 0:
        title_score *= 0.8

    description_score = 35
    if description_keyword_count > 0 and description_keyword_count < 4:
        description_score *= 1
    elif description_keyword_count > 3:
        description_score *= 0.5
    else:
        description_score *= 0

    h1_score = 30
    if h1_keyword_count > 0 and h1_keyword_count < 3:
        h1_score *= 1
    elif h1_keyword_count > 2:
        h1_score *= 0.5
    else:
        h1_score *= 0

    if h1_keyword_position > 0:
        h1_score *= 0.8

    # print('[Page score]')
    # print(f'title_score: {title_score}')
    # print(f'description_score: {description_score}')
    # print(f'h1_score: {h1_score}')
    return round(title_score + description_score + h1_score)


def get_density_str(density):
    return f"{density*100:.2f}%"


def get_words_stat(text, min_words_len=3, most_common_top=5):
    words_list = words_splitter.split(text.lower())
    words_list = list(filter(bool, words_list))

    words_count = len(words_list)

    words_list = filter(lambda x: len(x) >= min_words_len, words_list)
    top_words_list = Counter(words_list).most_common(most_common_top)
    top_list_stats = {
        word: {"Вхождений": count, "%": get_density_str(count / words_count)}
        for [word, count] in top_words_list
    }
    return top_list_stats


def get_words_count(value):
    return len(words_splitter.split(value))


def safe_run_with_default(func, default_value):
    try:
        return func()
    except Exception as e:
        print(e)
        return default_value


def get_stats_item(value):
    return {
        "Значение": value,
        "Число слов": get_words_count(value),
        "Число символов": len(value),
        "Статистика по словам": get_words_stat(value),
    }


def get_page_elements(url):
    client = HTMLSession()
    response = client.get(url)

    title = safe_run_with_default(
        lambda: response.html.find("title", first=True).text, ""
    )
    description = safe_run_with_default(
        lambda: response.html.find('meta[name="description"]', first=True).attrs[
            "content"
        ],
        "",
    )
    h1 = safe_run_with_default(lambda: response.html.find("h1", first=True).text, "")

    return {"title": title, "description": description, "h1": h1}


def get_page_stats(url):
    page_elements = get_page_elements(url)

    stats_info = {
        "url": url,
        "Заголовок страницы": get_stats_item(page_elements["title"]),
        "Описание": get_stats_item(page_elements["description"]),
        "Заголовок первого уровня": get_stats_item(page_elements["h1"]),
    }
    return stats_info


def main(url, keyword):
    page_elements = get_page_elements(url)
    page_score = calculate_score(
        keyword,
        title=page_elements["title"],
        description=page_elements["description"],
        h1=page_elements["h1"],
    )
    # print("Page stats:")
    # print(json.dumps(get_page_stats(url), indent=2, ensure_ascii=False))
    print(f"Page score: {page_score} / 100")

    while bool(keyword):
        keyword = input(
            "Можете проверить ту же страницу для другого ключа (Enter чтобы выйти): "
        ).strip()
        if not bool(keyword):
            break
        main(url, keyword)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze page information", add_help=False
    )
    parser.add_argument("url")
    parser.add_argument("keyword")
    args = parser.parse_args()

    url = args.url
    keyword = args.keyword

    assert url.startswith(
        "http"
    ), "Please check param value. Url should start with http(s)"
    assert bool(keyword), "Please provide proper keyword as second argument"

    try:
        main(url, keyword)
    except Exception as ex:
        print(f"Something went wrong: \n\n\n{str(ex)})\n\n\n - try another url")
