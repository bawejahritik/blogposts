import os
import yaml
import markdown
import click
import datetime

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

def handle_init():
    heading = input("Enter the heading of the post: ")
    description = input("Enter the description for the post: ")
    date = datetime.datetime.now()
    date = date.strftime("%B %d, %Y")
    
    idx = len(os.listdir(CONTENT_DIR))+1

    with open(f"{CONTENT_DIR}/post{idx}.yaml", "w") as f:
        data_to_write = f"heading: {heading}\ndate: {date}\ndescription: {description}\n-----\n" 
        f.write(data_to_write)
    print(f"Post file created at {CONTENT_DIR}/post{idx}.yaml. Open your favorite text editor and start writing.")

def handle_html():
    posts = get_all_posts()
    index_list = []
    for post in posts:
        filename, heading, date, html_content, description = get_description_and_content(post.name)
        generate_html_for_post(filename, heading, date, html_content)
        index_list.append([filename+".html", heading, date, description])

    generate_html_index(index_list[::-1])

@click.command()
@click.option('-i','--init', help='Initialize a new post', is_flag=True)
@click.option('-h', '--html', help='Generate html for new post', is_flag=True)
def main(init, html):
    if init:
        handle_init()

    if html:
        handle_html()

if __name__ == '__main__':
    main()
