from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from pandas import read_excel
from pprint import pprint

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
    params = [param for param in dictionary]
    return len(dictionary[params[0]])


def format_data(wine_number: int, dictionary: dict):
    data = [dictionary[param][wine_number] for param in dictionary]
    return data


wine_data = read_excel("wine.xlsx").to_dict()
wines_quantity = get_dict_length(wine_data)


env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape(["html", "xml"]),
)

template = env.get_template("template.html")

rendered_page = template.render(
    years_with_client = datetime.now().year-1920,
    define_word = word_define(datetime.now().year-1920),
    wines_quantity = wines_quantity,
    wine_data = wine_data,
    format_data = format_data
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
