"""
A simple static site generator for my GitHub pages site.

1. Place new markdown file in the articles directory.

2. Run this python script. The html directory will be updated with a new page and the
"""

import os

import mistune
from jinja2 import Environment, Template, FileSystemLoader

def extract_file_names(cwd: str) -> list[str]:
    paths = os.listdir(os.path.join(cwd, "articles"))
    return [file_name for file_name in paths if file_name.endswith(".md")]


def parse_article(cwd: str, file_name: str, article_template: Template):
    """Parse the article in the articles directory and insert into a html template."""
    with open(os.path.join(cwd, "articles", file_name), "r") as f:
        content = mistune.html(f.read())

    rendered = article_template.render(
        title=file_name.removesuffix(".md"),
        content=content,
    )

    new_title = file_name.replace(".md", ".html")
    with open(
        os.path.join(cwd, "html", new_title), mode="w", encoding="utf-8"
    ) as message:
        message.write(rendered)


def update_index(cwd: str, file_names: list[str], index_template: Template):
    """Update the index page with a list of all articles present"""

    rendered = index_template.render(
        articles=[file_name.replace(".md", ".html") for file_name in file_names],
    )

    with open(os.path.join(cwd, "index.html"), mode="w", encoding="utf-8") as message:
        message.write(rendered)


def generate_static_site():
    environment = Environment(loader=FileSystemLoader("templates/"))
    article_template = environment.get_template("article_template.html")
    index_template = environment.get_template("index_template.html")
    cwd = os.getcwd()

    file_names = extract_file_names(cwd)

    for name in file_names:
        parse_article(cwd, name, article_template)

    update_index(cwd, file_names, index_template)


if __name__ == "__main__":
    generate_static_site()
