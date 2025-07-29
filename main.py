from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from pandas import read_excel
from collections import defaultdict
from argparse import ArgumentParser


def define_word(years: int):
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


def get_drinks_quantity(drinks_info: dict):
    attributes = [attribute for attribute in drinks_info]
    return len(drinks_info[attributes[0]])


def format_attributes(drink_number: int, drinks_info: dict):
    attributes = [drinks_info[attribute][drink_number] for attribute in drinks_info]
    formatted_attributes = {
        "Картинка": attributes[4],
        "Категория": attributes[0],
        "Название": attributes[1],
        "Сорт": attributes[2],
        "Цена": attributes[3],
        "Акция": attributes[5]
    }
    return formatted_attributes


def main():
    parser = ArgumentParser(description="Парсер аргументов, для запуска сервера")
    parser.add_argument("--file", type=str, default="wine3.xlsx", help="Файл таблицы, из которого будут взяты данные")
    args = parser.parse_args()
    table_data = read_excel(args.file, na_values=["nan"], keep_default_na=False).to_dict()
    drinks_quantity = get_drinks_quantity(table_data)
    drinks_categories = defaultdict(list)
    for drink_number in range(drinks_quantity):
        current_drink = format_attributes(drink_number, table_data)
        category = current_drink["Категория"]
        drinks_categories[category].append(current_drink)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template("template.html")

    rendered_page = template.render(
        years_with_client = datetime.now().year-1920,
        define_word = define_word(datetime.now().year-1920),
        drinks_categories = drinks_categories
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()