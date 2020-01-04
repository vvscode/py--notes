from pprint import pprint


base_url = 'https://moz.com/blog'

# urls = list()
#
# for i in range(2, 377):
#     if (i % 10) == 0:
#         url = base_url + f'?page={i}'
#         urls.append(url)


urls = [base_url + f'?page={i}' for i in range(2, 377) if (i % 10) == 0]

pprint(urls)
