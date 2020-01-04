from time import sleep
from requests_html import HTMLSession


# domains_file = open('domains.txt', 'r', encoding='utf-8')
# text = domains_file.read()
# domains_file.close()


with open('domains.txt', 'r', encoding='utf-8') as domains_file:
    text = domains_file.read()


domains = [x.strip() for x in text.split('\n')]

# domains = list()
# for x in text.split('\n'):
#     domains.append(x.strip())


results = list()

for dom in domains:
    url = f'http://{dom}/'

    try:

        # session = HTMLSession()
        # response = session.get(url, timeout=8)
        # session.close()

        with HTMLSession() as session:
            response = session.get(url, timeout=8)

        print(response.status_code, dom)
        if response.status_code == 200:
            results.append(dom)

    except Exception as e:
        print(type(e), e)


print('All Domains: ', len(domains))
print('Norm Domains: ', len(results))
print(results)


result_text = '\n'.join(results)


# norm_dom_file = open('norm_domains.txt', 'w', encoding='utf-8')
# norm_dom_file.write(result_text)
# norm_dom_file.close()


with open('norm_domains.txt', 'w', encoding='utf-8') as norm_dom_file:
    norm_dom_file.write(result_text)


sleep(10000000)
