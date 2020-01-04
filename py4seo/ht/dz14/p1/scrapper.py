import logging
from urllib.parse import urlparse
import re
import csv

from requests_html import HTMLSession
from reppy.robots import Robots
from ozon_page import OzonPage
from robots_checker import RobotsChecker

import db


class Scrapper:
    website_structure = {}
    urls_queue = []
    _client = None

    def __init__(self, starting_page, pages_limit=20):
        self.starting_page = starting_page
        self.no_www_start_url = starting_page.replace("/www.", "/")
        self._robots_checker = None
        self.pages_limit = pages_limit

    def run(self):
        self.urls_queue = [(self.starting_page, 1)]
        while len(self.urls_queue):
            url_to_process, url_depth = self.urls_queue[0]
            self.urls_queue = self.urls_queue[1:]
            if self.should_link_be_processed(url_to_process):
                self.process_url(url_to_process, url_depth)

    def should_link_be_processed(self, link):
        pages_parsed_count = len(self.website_structure.keys())
        limit_reached = pages_parsed_count >= self.pages_limit
        no_www_link = link.replace("/www.", "/")
        should_be_processed = link.startswith("http")
        if self.no_www_start_url not in no_www_link:
            should_be_processed = False
        ret = (
            not limit_reached
            and should_be_processed
            and self.robots_checker.is_allowed(link)
        )
        logging.debug(
            f"Page should {'' if ret else 'NOT'} be processed: {link}. Limit: {pages_parsed_count}"
        )
        return ret

    def process_url(self, url_to_process, url_depth):
        page = OzonPage(url_to_process, client=self.client)
        self.website_structure[page.normalized_url] = {
            "url": page.normalized_url,
        }
        for link in page.links:
            logging.debug(f"Inner link: {link}")
            if link not in self.website_structure:
                self.urls_queue.append((link, url_depth + 1))

        if self.should_page_be_saved(url_to_process):
            try:
                category_rows = []
                for category in page.categories:
                    row = db.OzonCategory.insert(name=category).on_conflict_ignore().execute()
                    category_rows.append(row)

                product = db.OzonProduct.create(
                    url=page.normalized_url,
                    price=page.price,
                    title=page.title,
                    images='\n'.join(page.images)
                )

                product.categories.add(category_rows)

            except Exception as ex:
                print(f'Someting went wrong at {page.normalized_url}', ex)
                print('Probably you reached ad-product (no categories, usually it is some promotion)')

            logging.debug(f"Page {page.normalized_url} saved to db")

    def should_page_be_saved(self, url):
        return "/detail/" in url

    @property
    def client(self):
        if self._client is not None:
            return self._client
        self._client = HTMLSession()
        return self._client

    @property
    def robots_checker(self):
        if self._robots_checker is not None:
            return self._robots_checker
        self._robots_checker = RobotsChecker(self.starting_page)
        return self._robots_checker
