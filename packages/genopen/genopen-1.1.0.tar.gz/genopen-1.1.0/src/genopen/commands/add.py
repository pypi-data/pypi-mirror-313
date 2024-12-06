import os
from datetime import datetime
import click

def get_next_post_number(posts_dir):
    max_number = 0
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            try:
                post_number = int(filename.split('-')[0])
                max_number = max(max_number, post_number)
            except ValueError:
                continue
    return max_number + 1

def create_markdown_file(post_name):
    posts_dir = os.path.join('content', 'posts')
    os.makedirs(posts_dir, exist_ok=True)

    post_number = get_next_post_number(posts_dir)
    filename = f"{post_number}-{post_name.lower().replace(' ', '-')}.md"
    file_path = os.path.join(posts_dir, filename)

    current_datetime = datetime.now().astimezone().isoformat()
    yaml_header = (
        f"+++\n"
        f"date: {current_datetime}\n"
        f"updated_datetime: {current_datetime}\n"
        f"title: {post_name}\n"
        f"description: \"\"\n"
        f"+++\n\n"
        f"# {post_name}\n"
    )

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(yaml_header)

    return file_path

@click.command("add")
@click.argument("post_name")
def add_command(post_name):
    if not os.path.isfile('genopen.config'):
        click.echo("Error: 'genopen.config' not found. Make sure you are in a valid Genopen project folder.")
        return

    try:
        file_path = create_markdown_file(post_name)
        click.echo(f"Markdown file created at {file_path}")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
