import re
import json
import pprint
import argparse
from requests_html import HTMLSession
from collections import Counter

words_splitter = re.compile("\W")


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
        x = func()
        print("x", x)
        return x
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


def get_page_stats(url):
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

    stats_info = {
        "url": url,
        "Заголовок страницы": get_stats_item(title),
        "Описание": get_stats_item(description),
        "Заголовок первого уровня": get_stats_item(h1),
    }
    return stats_info


def main(url):
    stats = get_page_stats(url)

    print("json.dumps:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    print("pprint:")
    pprint.pprint(stats)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze page information", add_help=False
    )
    parser.add_argument("url")
    args = parser.parse_args()

    url = args.url

    if not url.startswith("http"):
        exit("Please check param value. Url should start with http(s)")

    try:
        main(url)
    except Exception as ex:
        print(f"Something went wrong: \n\n\n{str(ex)})\n\n\n - try another url")
