from csv import DictWriter
from pprint import pprint
from requests_html import HTMLSession


f = open('result_serpstat_keys.csv', 'w')
fieldnames = ['keyword', 'cost', 'region_queries_count']
writer = DictWriter(f, fieldnames=fieldnames)

writer.writeheader()


token = 'xxxxx'
se = 'g_ua'
api_method = 'keywords'
q = 'python'
page_size = 200
page = 1

for page in range(1, 5):

    print(f'Send request to {page} page')

    get_data = {
        'minus_keywords': 'django,free',
        'query': q,
        'token': token,
        'se': se,
        'page': page
    }

    api_url = f'https://api.serpstat.com/v3/{api_method}'

    with HTMLSession() as session:
        response = session.get(api_url, params=get_data)
    data = response.json()

    for hit in data['result']['hits']:

        # for key in hit:
        #     if key not in fieldnames:
        #         del hit[key]

        row = {k: v for k, v in hit.items() if k in fieldnames}
        writer.writerow(row)


print('All done!')
