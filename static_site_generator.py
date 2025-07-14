'''
WIP: deshittification coming soon.

A simple static site generator for my GitHub pages site. 

1. Place new markdown file in the articles directory.

2. Run this python script. The html directory will be updated with a new page and the 
'''

import os

import mistune
import jinja2


HTML = str


environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
template = environment.get_template("article_template.html")
index_template = environment.get_template("index_template.html")

def extract_article_paths(cwd: str) -> list[str]:
    articles = []
    for file_name in os.listdir(os.path.join(cwd, 'articles')):
        if file_name.endswith('.md'):
            articles.append(file_name)
    return articles


def parse_article(cwd: str, file_name: str) -> HTML:
    '''Parse the article in the articles directory and insert into a html template.'''
    with open(os.path.join(cwd, 'articles', file_name), 'r') as f:
        content = mistune.html(f.read())
    title = file_name.split('/')[-1]   

    new_title = title.replace('.md','.html')
    rendered = template.render(
        title=title.removesuffix('.md'),
        content=content,
    )
    with open(os.path.join(cwd, 'html', new_title), mode='w', encoding="utf-8") as message:
        message.write(rendered)


def update_index(cwd: str, file_names: list[str]):
    '''Update the index page with a list of all articles present'''
    
    rendered = index_template.render(
        articles=[file_name.replace('.md', '.html') for file_name in file_names],
    )

    with open(os.path.join(cwd, "index.html"), mode='w', encoding="utf-8") as message:
        message.write(rendered)
    


def generate_static_site():
    cwd = os.getcwd()

    article_paths = extract_article_paths(cwd)

    for path in article_paths:
        parse_article(cwd, path)

    update_index(cwd, article_paths)


if __name__ == "__main__":
    generate_static_site()
