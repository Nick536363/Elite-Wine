from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from pandas import read_excel
from pprint import pprint
from collections import defaultdict


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
    atributes = [atribute for atribute in dictionary]
    return len(dictionary[atributes[0]])


def format_data(drink_number: int, dictionary: dict):
    data = [dictionary[atribute][drink_number] for atribute in dictionary]
    dict_data = {
        "Картинка": data[4],
        "Категория": data[0],
        "Название": data[1],
        "Сорт": data[2],
        "Цена": data[3]
    }
    return dict_data


table_data = read_excel("wine2.xlsx").to_dict()
drinks_quantity = get_dict_length(table_data)
drinks_data = defaultdict(list)
for drink_number in range(drinks_quantity):
    current_drink = format_data(drink_number, table_data)
    category = current_drink["Категория"]
    drinks_data[category].append(current_drink)

pprint(drinks_data)

raise KeyError
env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape(["html", "xml"]),
)

template = env.get_template("template.html")

rendered_page = template.render(
    years_with_client = datetime.now().year-1920,
    define_word = word_define(datetime.now().year-1920),
    drinks_quantity = drinks_quantity,
    table_data = table_data,
    format_data = format_data
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
