from scrapper_utils import scrap_website, get_domain, save_pages_info

print(
    "Scrapper tool will parse your site starting with url and create sitemap csv file"
)
start_url = input("Enter start url (with protocol, like `http://ya.ru`): ").strip()
try:
    pages_info = scrap_website(start_url)
    output_filename = f"{get_domain(start_url)}.txt"
    result = save_pages_info(output_filename, pages_info)
    if result:
        print(f"Process finished. Check `{output_filename}` file")
    else:
        print(
            "Looks like no info collected. To check logs run script as `env LOGLEVEL=DEBUG python3 scrapper.py`"
        )
except Exception as e:
    print("Something went wrong with the process:")
    print(e)
