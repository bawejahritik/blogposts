import os
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.getcwd()
CONTENT_DIR = os.path.join(BASE_DIR, 'posts')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
GENERATED_POSTS_DIR = os.path.join(BASE_DIR, 'generated_posts')
ENV = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def generate_html_for_post(filename, heading, date, content):
    template = ENV.get_template("blog_post_template.html")
    html_content = template.render(
        heading = heading,
        date = date,
        content = content
    )

    with open(f"{GENERATED_POSTS_DIR}/{filename}.html", mode="w", encoding="utf-8") as message:
        message.write(html_content)
        print(f"... wrote {filename}")

def generate_html_index(posts):
    template = ENV.get_template("index_template.html")
    index_content = template.render(posts = posts)

    with open("index.html", mode="w", encoding="utf-8") as f:
        f.write(index_content)

def convert_from_yaml(data):
    yaml_dict = yaml.safe_load(data)
    return yaml_dict["heading"], yaml_dict["date"], yaml_dict["description"]

def convert_from_md(data):
    return markdown.markdown(data)

def get_all_posts():
    for entry in os.scandir(CONTENT_DIR):
        if entry.name.endswith('.yaml') and entry.is_file():
            yield entry

def get_description_and_content(filename):
    with open(os.path.join(CONTENT_DIR, filename)) as f:
        meta_data, content = f.read().split("-----", 1)

    heading, date, description = convert_from_yaml(meta_data)
    html_content = convert_from_md(content)
    filename, ext = os.path.splitext(filename)
    return filename, heading, date, html_content, description
     
def main():
    posts = get_all_posts()
    index_list = []
    for post in posts:
        filename, heading, date, html_content, description = get_description_and_content(post.name)
        generate_html_for_post(filename, heading, date, html_content)
        index_list.append([filename+".html", heading, date, description])

    generate_html_index(index_list[::-1])

if __name__ == '__main__':
    main()
