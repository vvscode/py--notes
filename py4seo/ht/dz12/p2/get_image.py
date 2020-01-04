from io import BytesIO

from requests_html import HTMLSession
from PIL import Image

client = HTMLSession()


def get_image_links_from_google(word, top=4):
    url = f"http://images.google.com/images?um=1&hl=en&safe=active&nfpr=1&q={word}"
    response = client.get(url)
    images = map(lambda response: response[0], response.html.search_all('"ou":"{}"'))
    return list(images)[:top]


def get_image_from_url(url):
    image = client.get(url)
    return Image.open(BytesIO(image.content))


def get_image(word, filename):
    top4_images_urls = get_image_links_from_google(word, top=4)
    top4_images = list(map(get_image_from_url, top4_images_urls))

    example_image = top4_images[0]

    quoter_height = example_image.height
    quoter_width = example_image.width

    resized_images = list(
        map(
            lambda image: image.resize((quoter_width, quoter_height), Image.ANTIALIAS),
            top4_images,
        )
    )

    sum_width = quoter_width * 2
    sum_height = quoter_height * 2

    new_im = Image.new("RGB", (sum_width, sum_height))

    new_im.paste(resized_images[0], (0, 0))
    new_im.paste(resized_images[1], (quoter_width, 0))
    new_im.paste(resized_images[2], (0, quoter_height))
    new_im.paste(resized_images[3], (quoter_width, quoter_height))

    new_im.save(filename, "JPEG")
