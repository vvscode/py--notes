import re
import os

from get_image import get_image

keyword = "гагарин"
while not bool(keyword):
    keyword = input("Enter keyword: ").strip()

filename = f'{re.sub(r"[^a-zA-Zа-яА-Я0-9_-]", "", keyword)}.jpeg'
get_image(keyword, filename)

os.system(f"open '{filename}'")
