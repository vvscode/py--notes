from timeit import default_timer as timer
import logging
import os
from urllib.parse import urlparse
import re
import csv

from requests_html import HTMLSession
from reppy.robots import Robots

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)


def get_robots_txt_checker(start_url, agent="Py4Seo Parse"):
    robots_txt_url = f"{start_url}/robots.txt".replace("//robots.txt", "/robots.txt")
    try:
        robots = Robots.fetch("robots_txt_url")
        agent = robots.agent(agent)
        return lambda url: agent.allowed(url)
    except:
        return lambda _: True


def safe_run_with_default(func, default_value):
    try:
        return func()
    except Exception as e:
        logging.debug(f"Some error on safe evaling: {e}")
        return default_value


def normalize_url(url):
    return url.split("#")[0]


def scrap_website(start_url):
    no_www_start_url = start_url.replace("/www.", "/")
    client = HTMLSession()
    website_structure = {}
    urls_queue = [(start_url, 1)]

    does_robots_txt_allow_to_parse = get_robots_txt_checker(start_url)

    def should_link_be_processed(link):
        no_www_link = link.replace("/www.", "/")
        should_be_processed = True
        if no_www_start_url in no_www_link:
            pass
        else:
            should_be_processed = False
        return should_be_processed and does_robots_txt_allow_to_parse(link)

    def process_url(url, depth):
        normalized_url = normalize_url(url)
        if not should_link_be_processed(normalized_url):
            return logging.debug(
                f"Url `{normalized_url}` is out of scope and would not be processed"
            )
        if normalized_url in website_structure:
            return logging.debug(f"Url already processed: {url_to_process}")

        logging.debug(f"Url to process: {url_to_process}")
        start_request_time = timer()
        response = client.get(normalized_url)
        end_request_time = timer()
        status_code = response.status_code
        title = safe_run_with_default(
            lambda: response.html.find("title", first=True).text, ""
        )
        h1 = safe_run_with_default(
            lambda: response.html.find("h1", first=True).text, ""
        )

        website_structure[normalized_url] = {
            "url": normalized_url,
            "depth": depth,
            "status code": status_code,
            "h1": h1,
            "title": title,
            "time to response": end_request_time - start_request_time,
        }

        for link in response.html.absolute_links:
            logging.debug(f"Inner link: {link}")
            if link not in website_structure:
                urls_queue.append((link, depth + 1))

    while len(urls_queue):
        url_to_process, url_depth = urls_queue[0]
        urls_queue = urls_queue[1:]

        process_url(url_to_process, url_depth)

    return list(website_structure.values())


def get_domain(url):
    try:
        parsed_uri = urlparse(url)
        return parsed_uri.netloc
    except:
        return re.sub("[^0-9a-zA-Z]+", "_", url)


def save_pages_info(file_name, pages_info):
    if not len(pages_info):
        print("No information to save")
        return False

    fieldnames = list(pages_info[0].keys())
    with open(file_name, "w") as output_file:
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for line in pages_info:
            csv_writer.writerow(line)
    return True
