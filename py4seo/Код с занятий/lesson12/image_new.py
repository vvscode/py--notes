import numpy
from requests_html import HTMLSession
from PIL import Image


url = 'https://d2v4zi8pl64nxt.cloudfront.net/advanced-techniques-to-pitch-guest-posts/5deefaf3e42f75.80738469.png'


def download_image(image_url):
    ftype = image_url.split('.')[-1]
    with HTMLSession() as session:
        response = session.get(image_url)
    with open(f'my_image.{ftype}', 'wb') as f:
        f.write(response.content)


img = Image.open('my_image.png')

print(img.format, img.size, img.mode)


new_w = int(img.size[0]/2)
new_h = int(img.size[1]/2)

# img = img.resize((new_w, new_h))
# img = img.rotate(2)

img = img.transpose(Image.TRANSPOSE)

# pixels = numpy.asarray(img)


img = img.convert('RGB')

img.save('resized_image4.webp')

# box = (100, 100, 400, 400)
# region = img2.crop(box)

# region.show()

img.show()

breakpoint()