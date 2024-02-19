import os
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.getcwd()
CONTENT_DIR = os.path.join(BASE_DIR, 'posts')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
GENERATED_POSTS_DIR = os.path.join(BASE_DIR, 'generated_posts')

def generate_html_for_post(filename, heading, date, content):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    print(env)
    template = env.get_template("blog_post.html")
    html_content = template.render(
        heading = heading,
        date = date,
        content = content
    )

    with open(f"{GENERATED_POSTS_DIR}/{filename}.html", mode="w", encoding="utf-8") as message:
        message.write(html_content)
        print(f"... wrote {filename}")


def convert_from_yaml(data):
    yaml_dict = yaml.safe_load(data)
    return yaml_dict["heading"], yaml_dict["date"]

def convert_from_md(data):
    return markdown.markdown(data)

def get_all_posts():
    for entry in os.scandir(CONTENT_DIR):
        if entry.name.endswith('.yaml') and entry.is_file():
            yield entry

def get_description_and_content(filename):
    with open(os.path.join(CONTENT_DIR, filename)) as f:
        description, content = f.read().split("-----", 1)

    heading, date = convert_from_yaml(description)
    html_content = convert_from_md(content)
    
    generate_html_for_post(filename[:-5], heading, date, html_content)
     

def main():
    posts = get_all_posts()
    for post in posts:
        get_description_and_content(post.name)

if __name__ == '__main__':
    main()
