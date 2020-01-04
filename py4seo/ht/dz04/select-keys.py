import argparse
import csv
import os


def main(file_name, keywords_list):
    output_file_name = f'{file_name}__{",".join(keywords_list)}__result.csv'

    fieldnames = ["keyword", "length", "words"]

    with open(file_name) as input_file, open(output_file_name, "a") as output_file:

        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        csv_writer.writeheader()

        for line in input_file:
            if any(keyword in line for keyword in keywords_list):
                keyword_line = line.strip()
                csv_writer.writerow(
                    {
                        "keyword": keyword_line,
                        "length": len(keyword_line),
                        "words": len(keyword_line.split()),
                    }
                )
    return output_file_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze page information", add_help=False
    )
    parser.add_argument("--file_name", default="./EnglishKeywords.txt")
    parser.add_argument("--keyword", default="")
    args = parser.parse_args()

    keyword_str = args.keyword
    file_name = args.file_name

    while not bool(keyword_str):
        keyword_str = input(
            "Enter one or multiple keywords (`,` as separator): "
        ).strip()

    keywords = [keyword.strip() for keyword in keyword_str.split(",")]

    try:
        assert len(keywords) > 0, "You have to provide at least one keyword"
        assert os.path.isfile(file_name), f"Database file {file_name} does not exist"

        output_file_name = main(file_name, keywords)
        print(f"Done. Check `{output_file_name}` file")
    except Exception as ex:
        print(f"Something went wrong: \n\n\n{str(ex)})\n\n")
