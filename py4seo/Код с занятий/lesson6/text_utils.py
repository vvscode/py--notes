from string import punctuation
from time import time


DOMAIN = 'py4you.com'


def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        res = func(*args, **kwargs)
        t2 = time()
        print('Время выполнения:', round(t2-t1, 4))
        return res
    return wrapper


@timer
def key_freq(text, n=10, *args, **kwargs):
    """
    Function to calculate words count in text.

    :param text: string
    :param n: length of results list
    :param args: positional params
    :param kwargs: kw params
    :return: list with words and count of each word
    """

    result = dict()
    text = text.lower()
    for p in punctuation:
        text = text.replace(p, ' ')
    for word in text.split():
        if len(word) < 4:
            continue
        if word not in result:
            result[word] = 1
        else:
            result[word] += 1
    result = list(result.items())
    result.sort(key=lambda x: x[1], reverse=True)
    return result[:n]


@timer
def print_A(a):
    print('AAAAAAAAAAAAA', a)


@timer
def print_B(b):
    print('BBBBBBBBBBBBB', b)
