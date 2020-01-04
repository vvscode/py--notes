import random
from time import time, sleep
from requests_html import HTMLSession
from googletrans import Translator
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost


class PBN:
    def __init__(self, keyword):
        self.keyword = keyword
        self.trans_articles = list()
        self.titles = list()
        self.posts = dict()
        self.trans_posts = dict()
        self.articles = list()
        self.trans_titles = list()

    def google_parser(self, keyword, user_agent):
        self.keyword = keyword
        url = f'https://www.google.com.ua/search?q={self.keyword}&num=100'
        headers = {'User-Agent': user_agent}
        with HTMLSession() as session:
            resp = session.get(url, headers=headers)
        return resp.html.xpath('//div[@class="r"]/a[1]/@href')

    def get_random_agent(self):
        with open('UA.txt') as f:
            agents = [x.strip() for x in f]
        return random.choice(agents)

    def main(self):
        # breakpoint()
        self.links = list()
        i = 0
        while True:
            if len(self.links) == 0:
                ua = self.get_random_agent()
                try:
                    print(f'Send request to GOOGLE [{self.keyword}] user_agent: {ua}')
                    self.links = self.google_parser(self.keyword, ua)
                except Exception as e:
                    print(type(e))
                print(f'Parsed {len(self.links)} URLs')
                i += 1
                if i>0 and len(self.links) == 0:
                    sleep(5)
            else:
                break

    def get_text(self):
        self.main()
        for link in self.links:
                if not len(self.articles) >= 3:
                    try:
                        with HTMLSession() as session:
                            resp = session.get(link, timeout = 5)
                    except:
                        print(f'Не удалось подключиться к {link} либо большой таймаут')
                    try:
                        article = resp.html.xpath('//p')[1].text
                        title = resp.html.xpath('//h1')[0].text
                        if len(article)>100 and len(title)>0:
                                if title not in self.titles:
                                    self.posts[title] = article
                                    self.titles.append(title)
                                    self.articles.append(article)
                                    print(f'Генерируем статью. Контент взят с {link}')
                                else:
                                    print('У статей одинаковые заголовки..ищем дальше')
                    except Exception as e:
                        print(f'Не достаточно контента на странице {link} или нету h1')
                else:
                    break

        return self.articles

    def translate(self):
        trans = Translator()
        for ttl, text in self.posts.items():
            trans_ttl = trans.translate(ttl)
            trans_text = trans.translate(text)
            self.trans_posts[trans_ttl.text] = trans_text.text
        print('Все статьи переведены!')

    def upload (self):
        wp_url = 'http://www.py4seo.com/xmlrpc.php'
        login = 'admin'
        passw = '123456'
        client = Client(wp_url, login, passw)
        posts = client.call(GetPosts({'number': 10000}))
        post = WordPressPost()
        for ttl, content in self.trans_posts.items():
            post.title = ttl
            post.content = content
            post.id = client.call(NewPost(post))
            post.post_status = 'publish'
            client.call(EditPost(post.id, post))
            url = f'http://py4seo.com/?p={post.id}'

            print(f'ЗАПОСТИЛИ СТАТЬЮ С ТАЙТЛОМ {ttl}' + ' - ' + url)


if __name__ == '__main__':
    print('!!!!!!!! Hello World !!!!!!')
    test_pbn = PBN('hello world')
    articles = test_pbn.get_text()
    print(articles)
