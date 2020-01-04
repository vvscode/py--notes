from string import punctuation


DOMAIN = 'py4you.com'


def key_freq(text, n=10, *args, **kwargs):
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


def print_A(a):
    print('AAAAAAAAAAAAA', a)


def print_B(b):
    print('BBBBBBBBBBBBB', b)
