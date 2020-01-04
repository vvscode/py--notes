from requests_html import HTMLSession

import argparse
import csv
import os


def get_position_info(keyword, domain):
    session = HTMLSession()
    serp_url = f"https://www.google.com/search?q={keyword}&num=100&hl=en"

    print(serp_url)

    resp = session.get(serp_url)

    links = resp.html.xpath('//div[@class="r"]/a[0]/@href')

    print(len(links))
    print(resp.html)

    for position, url in enumerate(links, start=1):
        print({domain, url})
        if domain in url:
            return (position, url)

    return (None, None)


def main(file_name, domain):
    output_file_name = f"{file_name}__{domain}__result.csv"

    fieldnames = ["keyword", "position", "url"]

    with open(file_name) as input_file, open(output_file_name, "a") as output_file:

        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        csv_writer.writeheader()

        for line in input_file:
            keyword = line.strip()
            position, url = get_position_info(keyword, domain)
            csv_writer.writerow(
                {"keyword": keyword, "position": position or "-", "url": url or "-",}
            )

    return output_file_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze page information", add_help=False
    )
    parser.add_argument("--file_name")
    parser.add_argument("--domain")
    args = parser.parse_args()

    domain = args.domain
    file_name = args.file_name

    try:
        assert "." in domain, f"Check domain `{domain}` format"
        assert os.path.isfile(file_name), f"Keywords file {file_name} does not exist"

        output_file_name = main(file_name, domain)
        print(f"Done. Check `{output_file_name}` file")
    except Exception as ex:
        print(f"Something went wrong: \n\n\n{str(ex)})\n\n")
