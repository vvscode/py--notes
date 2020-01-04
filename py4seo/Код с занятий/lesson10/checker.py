from requests_html import HTMLSession
from pprint import pprint


urls = [
    'https://py4you.com/courses/python-for-seo/',
    'https://py4you.com/courses/python-basic/',
    'https://py4you.com/courses/python-django/'
]


api_url = 'https://content-watch.ru/public/api/'
api_key = 'LaaZxj2RH0vRQDB'


with open('my_site_uniquness.csv', 'a') as f:
    for url in urls:
        post_data = {
            'action': 'CHECK_URL',
            'key': api_key,
            'url': url
        }

        with HTMLSession() as session:
            response = session.post(api_url, data=post_data)

        data = response.json()
        uniq = data["percent"]

        # ver 1
        # all_maches = data['matches']
        # all_urls = []
        # for match in all_maches:
        #     duplicate_url = match['url']
        #     all_urls.append(duplicate_url)
        # duplicate_urls_text = '\n'.join(all_urls)

        # ver 2
        all_duplicates = '\r\n'.join([x['url'] for x in data['matches']])

        pprint(data)

        f.write(f'"{url}"\t"{uniq}"\t"{all_duplicates}"\n')

print('All done!')

