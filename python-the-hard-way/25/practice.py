def break_words(stuff):
    '''this function will break up words for us'''
    return stuff.split(' ')


def sort_words(words):
    '''Sorts the words'''
    return sorted(words)


def print_first_word(words):
    '''print first word'''
    print(words.pop(0))


def print_last_word(words):
    '''print last words'''
    print(words.pop(-1))


def sort_sentence(sentence):
    '''takes in a full sentence and returns the sorted words'''
    words = break_words(sentence)
    return sort_words(words)


def print_first_and_last(sentence):
    '''print the first and the last words'''
    words = break_words(sentence)
    print_first_word(words)
    print_last_word(words)


def print_first_and_last_sorted(sentence):
    '''print the first/the last in sorted'''
    words = sort_sentence(sentence)
    print_first_word(words)
    print_last_word(words)
