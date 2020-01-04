from requests_html import HTMLSession
from reppy.robots import Robots

print('Start working')

domain = input('Enter domain name: ')
home_url = f'http://{domain}/'
robots_url = f'http://{domain}/robots.txt'

robots = Robots.fetch(robots_url)

links_to_scan = set()
links_to_scan.add(home_url)

scaned_links = set()

session = HTMLSession()

result_file = open('results.csv', 'w')
result_file.write(f'Is Duplicate\tURL\tTitle\tDescription\tH1\tCanonical\n')

all_titles = set()


def make(s):
    try:
        s = s[0].strip()
    except IndexError:
        s = ''
    return s


while len(links_to_scan) > 0:
    url = links_to_scan.pop()
    scaned_links.add(url)

    if not robots.allowed(url, '*'):
        continue

    try:
        print('SEND REQUEST TO: ', url)
        resp = session.get(url)
        links = resp.html.absolute_links
        print(f'Found {len(links)} links.')

        title = resp.html.xpath('//title/text()')
        description = resp.html.xpath('//meta[@name="description"]/@content')
        h1 = resp.html.xpath('//h1/text()')
        canonical = resp.html.xpath('//meta[@name="canonical"]/@rel')

        title = make(title)
        description = make(description)
        h1 = make(h1)
        canonical = make(canonical)

        duplicate = 'Yes' if hash(title) in all_titles else 'No'
        all_titles.add(hash(title))

        result_file.write(f'{duplicate}\t{url}\t{title}\t{description}\t{h1}\t{canonical}\n')

        links_to_scan = links_to_scan.union(links) - scaned_links
        print(f'Links to scan: {len(links_to_scan)}')
    except Exception as e:
        print(type(e), e)

result_file.close()

print('All Done!')
