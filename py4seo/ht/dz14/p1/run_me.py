import logging
import os
import re

from playhouse.postgres_ext import PostgresqlExtDatabase

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)

from scrapper import Scrapper

print(
    "Scrapper tool will parse your site starting with url and save data to DB"
)
start_url = "https://www.ozon.ru/"


def get_domain(url):
    try:
        parsed_uri = urlparse(url)
        return parsed_uri.netloc
    except:
        return re.sub("[^0-9a-zA-Z]+", "_", url)

Scrapper(start_url).run()

# try:
#     if Scrapper(start_url).run():
#         print(f"Process finished.")
#     else:
#         print(
#             "Looks like no info collected. To check logs run script as `env LOGLEVEL=DEBUG python3 run_me.py`"
#         )
# except Exception as e:
#     print("Something went wrong with the process:")
#     print(str(e))
