import numpy
from PIL import Image


class LogoImage:
    def __init__(self, file):
        self.file = file
        self.img = Image.open(file)
        self.pixels = [list(x) for x in numpy.array(self.img)]
        self._cursor = 0

    def __add__(self, other):
        images = [self.img, other.img]
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)
        new_im = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]
        result_name = self.file.split('.')[0] + '_' + \
                      other.file.split('.')[0] + '.' + \
                      other.file.split('.')[1]
        new_im.save(result_name)
        return LogoImage(result_name)

    def __iter__(self):
        return self

    def __next__(self, *args, **kwargs):
        if self._cursor + 1 >= len(self.pixels):
            raise StopIteration()
        self._cursor += 1
        return self.pixels[self._cursor]

    def __repr__(self):
        return f'Image: {self.file} | Pixels count: {len(self.pixels)}'

    def __len__(self):
        return len(self.pixels)

    def show_image(self):
        self.img.show()


logo1 = LogoImage('logo.png')
logo2 = LogoImage('logo2.png')


logo3 = logo1 + logo2


for pixel in logo3:
    print(pixel)

