from PIL import Image
from abc import ABCMeta, abstractmethod


class LogoImage(metaclass=ABCMeta):

    @abstractmethod
    def show_image(self, file):
        img = Image.open(file)
        img.show()

    @abstractmethod
    def download(self, url):
        pass


my_logo = LogoImage()
my_logo.show_image('logo.png')
