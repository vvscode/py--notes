from requests_html import HTMLSession
from reppy.robots import Robots


class Parser:

    def __init__(self, domain, schema):
        self.domain = domain
        self.schema = schema

        self.home_url = f'{self.schema}://{self.domain}/'
        self.robots_url = self.home_url + 'robots.txt'

        self.robots = Robots.fetch(self.robots_url)

        self.filename = domain.replace('.', '_') + '.csv'
        self.result_file = open(self.filename, 'w', encoding='utf-8')
        self.result_file.write('URL\tNAME\tPHONE\tPRICE\tAD_NUMBER\tAD_AUTHOR\tDESCRIPTION\n')

        # self.queue_urls = {self.home_url: 1}

        self.queue_urls = {
            'https://www.olx.ua/obyavlenie/zhestkiy-disk-dlya-noutbuka-hdd-2-5-'
            'sata-500gb-garantiya-aktsiya-IDFDRuU.html': 1
        }

        self.PARSED_URLS = set()

    def url_parser(self, url):
        with HTMLSession() as session:
            response = session.get(url, proxies={})

            if url.endswith('.html') and ('olx.ua/obyavlenie/' in url):
                ad_div = response.html.xpath('//div[@data-rel="phone"]/@class')[0]
                ad_div = eval(ad_div[ad_div.find('{'):ad_div.find('}')+1])
                ad_id = ad_div['id']
                token = response.html.xpath('//section[@id="body-container"]/script[1]')[0].text
                token = token.strip()[18:-2]
                phone_url = f'https://www.olx.ua/ajax/misc/contact/phone/{ad_id}/?pt={token}'
                response.html.render()
                response2 = session.get(phone_url)
                data = response2.json()
                phone = data['name']
            else:
                phone = None

        try:
            name = response.html.xpath('//h1')[0].text
        except Exception as e:
            name = 'not_found'
        try:
            price = response.html.xpath('//*[@id="offeractions"]/div[1]/strong/text()')
        except Exception as e:
            price = 'not_found'
        try:
            ad_number = response.html.xpath('//*[@id="offerdescription"]/div[2]/div[1]/em/small/text()')
        except Exception as e:
            ad_number = 'not_found'
        try:
            ad_author = response.html.xpath('//*[@id="offeractions"]/*/*/h4/a/text()')
        except Exception as e:
            ad_author = 'not_found'
        try:
            description = response.html.xpath('//*[@id="textContent"]/text()')
        except Exception as e:
            description = 'not_found'

        links = response.html.absolute_links

        return name, phone, price, ad_number, ad_author, description, links

    def link_filter(self, link):
        if '#' in link:
            link = link.split('#')[0]
        if link.endswith('.jpg'):
            return False
        if self.domain not in link:
            return False
        if link in self.PARSED_URLS:
            return False
        if not self.robots.allowed(link, '*'):
            return False
        return True

    def main(self):
        while len(self.queue_urls) > 0:

            min_level = min(self.queue_urls.values())

            for url, level in self.queue_urls.items():
                if level == min_level:
                    self.queue_urls.pop(url)
                    break

            print('Scan:', url, level)

            self.PARSED_URLS.add(url)

            name, phone, price, ad_number, ad_author, description, links = self.url_parser(url)

            if url.endswith('.html') and ('olx.ua/obyavlenie/' in url):
                result = f'{url}\t{name}\t{phone}\t{price}\t{ad_number}\t{ad_author}\t{description}\n'
                self.result_file.write(result)

            for link in links:
                if not self.link_filter(link):
                    continue

                if link not in self.queue_urls:
                    self.queue_urls[link] = level + 1


if __name__ == '__main__':
    domain = 'www.olx.ua'
    proto = 'https'

    pr = Parser(domain, proto)
    pr.main()
