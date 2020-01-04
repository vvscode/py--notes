import numpy
from time import time
from PIL import Image


def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print('Working time is: ', t2-t1)
        return result
    return wrapper


class LogoImage:

    @timer
    def __init__(self, file):
        self.file = file
        self.img = Image.open(file)

    def show_image(self):
        self.img.show()

    @property
    def pixels(self):
        return len(numpy.array(self.img))

    @staticmethod
    def something():
        print(123213)
        print('asdasdasdasd')
        print('rrtyrtyrtyrty')

    @classmethod
    def something2(cls):
        print(34634435)
        print('ghjgjghjghj')
        print('bnmbnmbnmbnm')


logo1 = LogoImage('logo.png')
