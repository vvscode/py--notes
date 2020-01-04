import logging
import os
import re

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)

from scrapper import Scrapper

print(
    "Scrapper tool will parse your site starting with url and create sitemap csv file"
)
start_url = (
    input("Enter start url (with protocol, like `http://ya.ru`): ").strip()
    or "https://py4you.com"
)


def get_domain(url):
    try:
        parsed_uri = urlparse(url)
        return parsed_uri.netloc
    except:
        return re.sub("[^0-9a-zA-Z]+", "_", url)


try:
    output_filename = f"{get_domain(start_url)}.csv"
    if Scrapper(start_url).run(output_filename):
        print(f"Process finished. Check `{output_filename}` file")
    else:
        print(
            "Looks like no info collected. To check logs run script as `env LOGLEVEL=DEBUG python3 scrapper.py`"
        )
except Exception as e:
    print("Something went wrong with the process:")
    print(str(e))
