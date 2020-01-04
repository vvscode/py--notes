import logging
from urllib.parse import urlparse
import re
import csv

from requests_html import HTMLSession
from reppy.robots import Robots
from page import Page
from robots_checker import RobotsChecker


class Scrapper:
    website_structure = {}
    urls_queue = []
    _client = None

    def __init__(self, starting_page):
        self.starting_page = starting_page
        self.no_www_start_url = starting_page.replace("/www.", "/")
        self._robots_checker = None

    def run(self, file_name):
        self.urls_queue = [(self.starting_page, 1)]
        while len(self.urls_queue):
            url_to_process, url_depth = self.urls_queue[0]
            self.urls_queue = self.urls_queue[1:]
            if self.should_link_be_processed(url_to_process):
                self.process_url(url_to_process, url_depth)
        return self.save_to_file(file_name)

    def should_link_be_processed(self, link):
        no_www_link = link.replace("/www.", "/")
        should_be_processed = link.startswith("http")
        if self.no_www_start_url not in no_www_link:
            should_be_processed = False
        return should_be_processed and self.robots_checker.is_allowed(link)


    def process_url(self, url_to_process, url_depth):
        page = Page(url_to_process, client=self.client)
        self.website_structure[page.normalized_url] = {
            "url": page.normalized_url,
            "depth": url_depth,
            "status code": page.status_code,
            "h1": page.h1,
            "title": page.title,
            "time to response": page.response_time,
        }
        for link in page.links:
            logging.debug(f"Inner link: {link}")
            if link not in self.website_structure:
                self.urls_queue.append((link, url_depth + 1))

    def save_to_file(self, file_name):
        pages_info = list(self.website_structure.values())
        if not len(pages_info):
            logging.debug("No information to save")
            return False

        fieldnames = list(pages_info[0].keys())
        with open(file_name, "w") as output_file:
            csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for line in pages_info:
                csv_writer.writerow(line)
        return True

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
