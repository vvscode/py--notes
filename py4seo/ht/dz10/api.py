from requests_html import HTMLSession

client = HTMLSession()
photos_page = client.get('https://jsonplaceholder.typicode.com/photos')
photos_urls = [x['url'] for x in photos_page.json()]
with open('photos.txt', 'w') as fp:
  fp.writelines(map(lambda x: f'{x}\n', photos_urls))

print(f'{len(photos_urls)} photos loaded')