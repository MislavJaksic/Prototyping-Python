"""
    protopy.py
    ------------------

    Runs the project.

    :copyrgiht: 2019 MislavJaksic
    :license: MIT License
"""
import datetime
import sys

from rapdevpy import lxml_lib

"""
Getting data:
* [Visit](https://pretinac.gov.hr/KorisnickiPretinac/eGradani.html)
* right click
* Inspect Element
* right click on "html" element in second row
* "Copy", then "Outer HTML"
* paste into a `*.html` (do not format it!)

Bizzarly, XPATHs start with `/body`, not `/html`!
"""


class EGradaniParser:
    def __init__(self, input_filename, output_filename, top_xpath, headers):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.headers = headers
        self.top_xpath = top_xpath
        self.row_delimiter = "\n"
        self.tree = lxml_lib.load_tree(self.input_filename)
        self.root = lxml_lib.get_root(self.tree)
        self.services_in_categories = lxml_lib.find_all_by_xpath(
            self.tree, self.top_xpath
        )
        csv_strings = []
        for services_in_category in self.services_in_categories:
            category, services = self.parse_services_in_category(services_in_category)
            for service in services:
                name, href, description = self.parse_service(service)
                csv_string = self.stringify(category, name, href, description)
                csv_strings.append(csv_string)

        self.write(csv_strings)

    def parse_services_in_category(self, services_in_category):
        category = services_in_category.find("h3").text
        services = services_in_category.findall("ul/li/a")
        return category, services

    def parse_service(self, service):
        name = service.text
        href = service.get("href")
        title = service.get("title")
        title_delimiter = self.row_delimiter
        key_values = title.split(title_delimiter, maxsplit=3)
        description = self.parse_key_value(key_values)
        return name, href, description

    def parse_key_value(self, key_values):
        dict = {}
        for key_value in key_values:
            compact_key_value = key_value.replace(self.row_delimiter, "")
            key_and_value = compact_key_value.split(": ", maxsplit=1)
            dict[key_and_value[0]] = key_and_value[1]
        return dict

    def stringify(self, category, name, href, description):
        csv_string = ""
        csv_string = csv_string + category + "$"
        csv_string = csv_string + name + "$"
        csv_string = csv_string + href + "$"

        csv_string = csv_string + description["Pružatelj"] + "$"
        date_time_obj = datetime.datetime.strptime(
            description["Usluga aktivna od"], "%d.%m.%Y."
        )
        csv_string = csv_string + str(date_time_obj.date()) + "$"
        csv_string = csv_string + description["Razina autentifikacije"] + "$"
        csv_string = csv_string + description["Opis"]
        return csv_string

    def write(self, csv_strings):
        with open(self.output_filename, "w", encoding="utf-8") as file:
            file.write(self.headers + "\n")
            for string in csv_strings:
                file.write(string)
                file.write("\n")


def main(args):
    """main() will be run if you run this script directly"""
    EGradaniParser(
        "protopy/egradani_parser/data/egradani-dostupne.html",
        "output-dostupne.csv",
        "/body/div[3]/div/div[4]/div",
        "Kategorija$Usluga$Poveznica$Pružatelj$Usluga aktivna od$Razina autentifikacije$Opis",
    )
    EGradaniParser(
        "protopy/egradani_parser/data/egradani-ostale.html",
        "output-ostale.csv",
        "/body/div[3]/div/div[7]/div",
        "Kategorija$Usluga$Poveznica$Pružatelj$Usluga aktivna od$Razina autentifikacije$Opis",
    )


def run():
    """Entry point for the runnable script."""
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run()."""
    run()
