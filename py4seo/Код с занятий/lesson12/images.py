from PIL import Image
from requests_html import HTMLSession


url = 'http://www.reallifestories.org/wp-content/uploads/2018/04/Gagarin-1-648x487.jpg'
session = HTMLSession()
resp = session.get(url)
ext = url.split('.')[-1]

with open(f'my_image.{ext}', 'wb') as f:
    f.write(resp.content)

print('All Done!')

# breakpoint()

# img = Image.open(f'my_image.{ext}')
#
# w, h = img.size
#
# img = img.rotate(3)
#
# area = (20, 20, w-20, h-20)
#
# cutted = img.crop(area)
#
# cutted.save('cutted.jpg')


img1 = Image.open('cutted.jpg')
img2 = Image.open('gagarin.jpg')

h1, w1 = img1.size
w2 = img2.width

image3 = Image.new('RGB', (w1+w2, h1))

image3.paste(img1, (0, 0))

h2, w2 = img2.size

X = int((h1 / h2) * w2)

img2.resize((X, h1), 1)

image3.paste(img2, (w1, 0))

image3.show()

image3.save('asdasdasd.png')

breakpoint()
