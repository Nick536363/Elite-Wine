from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from pandas import read_excel
from collections import defaultdict
from argparse import ArgumentParser


def word_define(years: int):
    str_year = str(years)
    condition = {
        "0": "лет",
        "1": "год",
        "2": "года",
        "3": "года",
        "4": "года"
    }
    if str_year[-2] == "1":
        return "лет"
    else:
        try:
            return condition[str_year[-1]]
        except KeyError:
            return "лет"


def get_dict_length(dictionary: dict):
    attributes = [attribute for attribute in dictionary]
    return len(dictionary[attributes[0]])


def format_data(drink_number: int, dictionary: dict):
    data = [dictionary[atribute][drink_number] for atribute in dictionary]
    dict_data = {
        "Картинка": data[4],
        "Категория": data[0],
        "Название": data[1],
        "Сорт": data[2],
        "Цена": data[3],
        "Акция": data[5]
    }
    return dict_data


def main():
    parser = ArgumentParser(description="Парсер аргументов, для запуска сервера")
    parser.add_argument("--file", type=str, default="wine3.xlsx", help="Файл таблицы, из которого будут взяты данные")
    args = parser.parse_args()
    table_data = read_excel(args.file, na_values=["nan"], keep_default_na=False).to_dict()
    drinks_quantity = get_dict_length(table_data)
    drinks_data = defaultdict(list)
    for drink_number in range(drinks_quantity):
        current_drink = format_data(drink_number, table_data)
        category = current_drink["Категория"]
        drinks_data[category].append(current_drink)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template("template.html")

    rendered_page = template.render(
        years_with_client = datetime.now().year-1920,
        define_word = word_define(datetime.now().year-1920),
        drinks_data = drinks_data
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()