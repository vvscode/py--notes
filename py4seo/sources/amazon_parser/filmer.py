import os
import io
import requests
from PIL import Image
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from lxml import html
from selenium import webdriver
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts


MY_WP_SITE = 'http://bestmoviestorent.com/xmlrpc.php'
MY_WP_LOGIN = 'chernenko'
MY_WP_PASS = '0919963996'


def init_queue(q):
    with open('film_links2.txt', 'r', encoding='utf-8') as f:
        all_films = set([line for line in f if line])
    with open('done_films.txt', 'r', encoding='utf-8') as f:
        done_films = set([line for line in f if line])
    with open('error_films.txt', 'r', encoding='utf-8') as f:
        error_films = set([line for line in f if line])
    with open('serials_films.txt', 'r', encoding='utf-8') as f:
        serials_films = set([line for line in f if line])
    films = all_films - done_films - error_films - serials_films
    for f in films:
        q.put(f.strip())
    print(q.qsize())


def parse_film_and_save(q):
    chrome_driver = os.path.join(os.getcwd(), 'chromedriver.exe')
    browser = webdriver.Chrome(executable_path=chrome_driver)
    wp = Client(MY_WP_SITE, MY_WP_LOGIN, MY_WP_PASS)

    while q.qsize():
        url = q.get()
        # url = 'https://www.amazon.com/Happy-Ones-Zach-Matchem/dp/B0749CK18F/'
        # pdb.set_trace()
        browser.get(url)
        if 'id="dv-episode-list"' in browser.page_source:
            with open('serials_films.txt', 'a', encoding='utf-8') as f:
                f.write(url + '\n')
            continue
        tree = html.fromstring(browser.page_source)
        try:
            film = dict()
            film['purchase'] = []
            film['category'] = []
            film['movie_outlink'] = url

            film['title'] = str(tree.xpath('//h1/text()')[0].strip())
            film['movie_poster'] = str(tree.xpath('//div[@class="dp-meta-icon-container"]/img/@src')[0].strip())

            try:
                film['content'] = str(tree.xpath('//div[contains(@class, "dv-simple-synopsis")]/p/text()')[0].strip())
            except Exception:
                film['content'] = ''

            try:
                film['movie_imdb_rating'] = str(tree.xpath('//span[@class="imdb-rating"]/strong/text()')[0].strip())
            except Exception:
                film['movie_imdb_rating'] = '0'

            try:
                film['movie_star_rating'] = str(tree.xpath('//i[@id="reviewStars"]/span/text()')[0].strip())[:3]
            except Exception:
                film['movie_star_rating'] = '0.0'

            try:
                film['movie_votes'] = str(tree.xpath('//span[@id="reviewLink"]/a/text()')[0].strip()).replace(',', '')
            except Exception:
                film['movie_votes'] = '0'

            try:
                film['movie_price_buy'] = str(
                    [x[x.index('$')+1:].strip() for x in tree.xpath('//div[@class="dv-button-text"]/text()') if
                     'Buy' in x][0])
                film['purchase'].append('Buy')
            except Exception:
                film['movie_price_buy'] = '0'

            try:
                film['movie_price_rent'] = str(
                    [x[x.index('$') + 1:].strip() for x in tree.xpath('//div[@class="dv-button-text"]/text()') if
                     'Rent' in x][0])
                film['purchase'].append('Rent')
            except Exception:
                film['movie_price_rent'] = '0'

            for i in range(1, 7):
                data = tree.xpath('//table[contains(@class, "a-keyvalue")]/tbody/tr[{}]/th[1]/text()'.format(i))
                if len(data) > 0:
                    data = str(data[0]).strip().lower()
                    film[data] = [str(x).strip() for x in tree.xpath('//table[contains(@class, "a-keyvalue")]/tbody/tr[{}]/td[1]/a/text()'.format(i))]

            film['years'] = [str(x).strip() for x in tree.xpath('//h1/span[@class="release-year"]/text()')]

            if float(film['movie_imdb_rating']) > 8.5:
                film['category'].append('Best of movies')
            if int(film['movie_votes']) > 300:
                film['category'].append('Best Sellers')
            if len(film['years']) > 0:
                if int(film['years'][0]) < 2000:
                    film['category'].append('Classic movies')
            if film['movie_price_buy'] == '0' and film['movie_price_rent'] == '0':
                film['category'].append('Free with Ads')
            if '2017' in film['years'] or '2018' in film['years']:
                film['category'].append('Hot New Releases')
            if 100 < int(film['movie_votes']) < 300:
                film['category'].append('Popular movies')
            if int(film['movie_votes']) > 200 and '2017' in film['years']:
                film['category'].append('Trending movies')
            if len(film['category']) == 0:
                film['category'].append('Exclusive movies')

            image_byte = requests.get(film['movie_poster']).content
            img = Image.open(io.BytesIO(image_byte))
            if img.size[1] < 250:
                raise ValueError('Bad image size')

            # keyword = film['title'].lower() + ' movie'
            # film['movie_secondary_description'] = generate_content(keyword)

            if not film.get('category'):
                film['category'] = []
            if not film.get('director'):
                film['director'] = []
            if not film.get('genres'):
                film['genres'] = []
            if not film.get('purchase'):
                film['purchase'] = []
            if not film.get('starring'):
                film['starring'] = []
            if not film.get('years'):
                film['years'] = []

        except Exception as e:
            print(type(e), e, '[Error in parser]')
            # browser.quit()
            # browser = webdriver.Chrome(executable_path=chrome_driver)
            with open('error_films.txt', 'a', encoding='utf-8') as f:
                f.write(url + '\n')
            continue

        try:
            post = WordPressPost()
            post.title = film['title']
            post.content = film['content']
            post.post_status = 'publish'

            post.id = wp.call(posts.NewPost(post))
            print('[OK] post id ', post.id)
        except Exception as e:
            print(type(e), e, '[Error in film saving]')
            with open('error_films.txt', 'a', encoding='utf-8') as f:
                f.write(url + '\n')
            continue

        with open('done_films.txt', 'a', encoding='utf-8') as f:
            f.write(url+'\n')


def main():
    treads = 4
    q = Queue()
    init_queue(q)
    with ThreadPoolExecutor(max_workers=treads) as executor:
        for _ in range(treads):
            executor.submit(parse_film_and_save, q)


if __name__ == '__main__':
    main()
