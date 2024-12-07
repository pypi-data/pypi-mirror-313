from bs4 import BeautifulSoup
from myfletify.parser import parse_html_to_flet


def convert_html_to_flet(html_file):
    with open(file=html_file, mode="r") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    flet_code = parse_html_to_flet(soup)
    return flet_code
