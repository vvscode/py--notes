from requests_html import HTMLSession


def serp_parser(key, domain='py4you.com'):

    print('Send request:', key)

    with HTMLSession() as session:
        try:
            resp = session.get(
                f'https://www.google.com/search?q={key}&num=100&hl=en')
            if resp.status_code != 200:
                raise ValueError('Status code is not 200')
            links = resp.html.xpath('//div[@class="r"]/a[1]/@href')
            found = 'not_found'
        except Exception as e:
            print(type(e), e)
            links = []
            found = 'ban_google'

    result = [key, found, '-']

    for position, url in enumerate(links, 1):
        if domain in url:
            result = [key, url, position]

    return result
