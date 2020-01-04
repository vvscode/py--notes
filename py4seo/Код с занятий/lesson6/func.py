# import text_utils

import random as rd

from slugify import *
from text_utils import key_freq
from utils.text import DOMAIN as DOM


DOMAIN = 'rozetka.com.ua'


TEXT = '''
Python is an interpreted, high-level, general-purpose programming language. 
Created by Guido van Rossum and first released in 1991, Python's design philosophy 
emphasizes code readability with its notable use of significant whitespace. Its 
language constructs and object-oriented approach aim to help programmers write 
clear, logical code for small and large-scale projects.[27]

Python is dynamically typed and garbage-collected. It supports multiple programming 
paradigms, including procedural, object-oriented, and functional programming. 
Python is often described as a "batteries included" language due to its 
comprehensive standard library.[28]

Python was conceived in the late 1980s as a successor to the ABC language. 
Python 2.0, released in 2000, introduced features like list comprehensions and 
a garbage collection system capable of collecting reference cycles. Python 3.0, 
released in 2008, was a major revision of the language that is not completely 
backward-compatible, and much Python 2 code does not run unmodified on Python 3.

The Python 2 language, i.e. Python 2.7.x, is "sunsetting" on January 1, 2020 
(after extension; first planned for 2015), and the Python team of volunteers 
will not fix security issues, or improve it in other ways after that date.
With the end-of-life, only Python 3.5.x and later will be supported.

Python interpreters are available for many operating systems. A global 
community of programmers develops and maintains CPython, an open source 
reference implementation. A non-profit organization, the Python Software Foundation, 
manages and directs resources for Python and CPython development.
'''

keys = key_freq(TEXT, 10, 1000, 'qweqweqwe', alpha=1000, beta='asdasds')


print(DOM, DOMAIN)


name = 'Python interpreters are available for many operating systems'
slug = slugify(name, stopwords=('for', 'are'))


print(slug, rd.randint(1, 10))


s = ['python', 'for', 'you']


def mutate(text):
    s.sort()
    print(len(text.split()), 'количество слов в тексте.')
    print(s)


mutate('hello world')

print(s)
