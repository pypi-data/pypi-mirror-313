import os
import shutil
import fnmatch
import re
from datetime import datetime
import markdown
import yaml
import click
import locale

class MarkdownToBlogGenerator:
    def __init__(self, config_path='genopen.config'):
        self.load_config(config_path)
        self.setup_paths()
        self.load_theme()

    def load_config(self, config_path):
        try:
            with open(config_path, 'r', encoding="utf-8") as config_file:
                self.global_variables = yaml.safe_load(config_file)

                if 'theme' not in self.global_variables:
                    raise KeyError("Missing 'theme' variable in genopen.config")

                self.global_variables["current_year"] = str(
                    datetime.now().year)
                self.theme_name = self.global_variables['theme']

                if "environment_prefix" in self.global_variables and self.global_variables["environment_prefix"]:
                    prefix = self.global_variables["environment_prefix"]

                    for key, value in os.environ.items():
                        if key.startswith(prefix):
                            key = key.replace(prefix, "ENV")
                            self.global_variables[key] = value

                locale.setlocale(locale.LC_TIME, self.global_variables["locale"])

        except KeyError as e:
            raise KeyError(f"Error: {e}. Please check your genopen.config file.")

    def setup_paths(self):
        self.theme_path = os.path.join('themes', self.theme_name)
        self.content_path = "content"
        self.content_posts_path = os.path.join(self.content_path, 'posts')
        self.content_assets_path = os.path.join(self.content_path, 'assets')
        self.output_web_path = "web"

    def load_theme(self):
        self.theme_files = {}

        for root, _, files in os.walk(self.theme_path):
            for file in files:
                relative_path = os.path.relpath(
                    os.path.join(root, file), self.theme_path)

                if (os.path.splitext(relative_path)[1] == ".html"):
                    with open(os.path.join(root, file), 'r', encoding="utf-8") as f:
                        content = f.read()
                else:
                    content = relative_path

                self.theme_files[relative_path] = content

    def copy_static_files(self):
        output_web_assets_path = os.path.join(self.output_web_path, "assets")
        os.makedirs(output_web_assets_path, exist_ok=True)

        for file_path in self.theme_files:
            if not file_path.endswith('.html'):
                output_path = os.path.join(self.output_web_path, file_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                theme_file_path = os.path.join(self.theme_path, file_path)
                shutil.copy2(theme_file_path, output_path)

        for filename in os.listdir(self.content_assets_path):
            original_filepath = os.path.join(
                self.content_assets_path, filename)
            output_assets_filepath = os.path.join(
                output_web_assets_path, filename)
            shutil.copy2(original_filepath, output_assets_filepath)

    def load_posts(self):
        self.posts = []
        for filename in os.listdir(self.content_posts_path):
            if filename.endswith('.md'):
                post_path = os.path.join(self.content_posts_path, filename)

                with open(post_path, 'r', encoding="utf-8") as f:
                    post_content = f.read()

                metadata = {}
                content_without_metadata = post_content
                if post_content.startswith('+++\n'):
                    parts = post_content.split('+++\n', 2)
                    if len(parts) > 1:
                        try:
                            metadata = yaml.safe_load(parts[1])
                            metadata['datetime'] = metadata['date']
                            metadata['date'] = metadata['datetime'].strftime(self.global_variables["date_format"])
                            content_without_metadata = parts[2]
                        except yaml.YAMLError as e:
                            print(
                                f"Error parsing YAML front matter in {filename}: {e}")

                base_filename = os.path.splitext(filename)[0]
                image_path = None
                for file in os.listdir(self.content_assets_path):
                    if os.path.splitext(file)[0] == base_filename:
                        image_path = os.path.join(
                            self.content_assets_path, file)
                        metadata['image'] = f"assets/{file}"
                        metadata[
                            'alt_image'] = f"Logo showing theme of page {base_filename.replace('-', ' ')}"
                        break
                if image_path == None:
                    metadata['image'] = f"assets/empty.png"
                    metadata['alt_image'] = f"No image, coming soon"

                metadata['url'] = f"pages/{base_filename}.html"
                metadata['markdown'] = markdown.markdown(
                    content_without_metadata)
                post = {
                    'filepath': post_path,
                    'filename': base_filename,
                    'metadata': metadata,
                    'content': content_without_metadata,
                    'image_path': image_path
                }
                self.posts.append(post)

        self.posts.sort(
            key=lambda post: post['metadata']['datetime'], reverse=True)

    def load_sub_files(self, parent_file):
        result = {}
        pattern = f"{parent_file}.*.html"

        for file in self.theme_files:
            if fnmatch.fnmatch(file, pattern):
                sub_file_posts = []

                for post in self.posts:
                    post_html = self.theme_files[file]

                    for variable in self.global_variables:
                        post_html = post_html.replace(
                            f"{{{{{variable}}}}}", str(self.global_variables[variable]))

                    for variable in post['metadata']:
                        post_html = post_html.replace(
                            f"{{{{{variable}}}}}", str(post['metadata'][variable]))

                    sub_file_posts.append(post_html)

                result[file] = '\n'.join(sub_file_posts)

        return result

    def generate_pages(self):
        pattern = re.compile(r"^(?!post\.html$)[^.]+\.html$")

        for file in self.theme_files:
            if pattern.match(file):
                self.global_variables.update(
                    self.load_sub_files(os.path.splitext(file)[0]))
                page_content = self.theme_files[file]

                for variable in self.global_variables:
                    page_content = page_content.replace(
                        f"{{{{{variable}}}}}", str(self.global_variables[variable]))

                page_output_path = os.path.join(self.output_web_path, file)
                with open(page_output_path, 'w', encoding='utf-8') as f:
                    f.write(page_content)
                    self.sitemaps.append(
                        {
                            "url": file,
                            "updated_at": datetime.fromtimestamp(os.path.getmtime(os.path.join(self.theme_path, file)))
                        }
                    )

    def generate_post_pages(self):
        if 'post.html' not in self.theme_files:
            raise FileNotFoundError(
                "Error: 'post.html' file is missing in the theme.")

        output_web_pages_path = os.path.join(self.output_web_path, "pages")
        os.makedirs(output_web_pages_path, exist_ok=True)

        post_content = self.theme_files['post.html']
        for post in self.posts:
            html_content = post_content
            for variable in self.global_variables:
                html_content = html_content.replace(
                    f"{{{{{variable}}}}}", str(self.global_variables[variable]))

            for variable in post['metadata']:
                html_content = html_content.replace(
                    f"{{{{{variable}}}}}", str(post['metadata'][variable]))

            page_output_path = os.path.join(
                output_web_pages_path, f"{post['filename']}.html")
            with open(page_output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                self.sitemaps.append(
                    {
                        "url": post['metadata']['url'],
                        "updated_at": post['metadata']['updated_datetime']
                    }
                )

    def generate_site_maps(self):
        sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        for file in self.sitemaps:
            if file['url'] == 'index.html':
                page_url = self.global_variables['domain']
            else:
                page_url = f"{self.global_variables['domain']}/{file['url']}"
            page_url_last_update = file['updated_at'].strftime("%Y-%m-%d")

            sitemap_content += f"  <url>\n"
            sitemap_content += f"    <loc>{page_url}</loc>\n"
            sitemap_content += f"    <lastmod>{page_url_last_update}</lastmod>\n"
            sitemap_content += f"  </url>\n"

        sitemap_content += '</urlset>'

        sitemap_path = os.path.join(self.output_web_path, 'sitemap.xml')
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)

    def generate_rss(self):
        if self.global_variables.get('generate_rss'):
            rss_content = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
            rss_content += "<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">\n"
            rss_content += "<channel>\n"
            rss_content += f"    <title>{self.global_variables['blog_name']}</title>\n"
            rss_content += f"    <link>{self.global_variables['domain']}</link>\n"
            rss_content += f"    <description>{self.global_variables['blog_description']}</description>\n"
            rss_content += "    <language>fr-FR</language>\n"
            rss_content += f"    <pubDate>{self.posts[0]['metadata']['updated_datetime'].strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate>\n"
            rss_content += f"    <atom:link href=\"{self.global_variables['domain']}/rss.xml\" rel=\"self\" type=\"application/rss+xml\" />\n"

            for post in self.posts:
                post_image_url = f"{self.global_variables['domain']}/{post['metadata']['image']}"
                rss_content += "    <item>\n"
                rss_content += f"        <title>{post['metadata']['title']}</title>\n"
                rss_content += f"        <link>{self.global_variables['domain']}/{post['metadata']['url']}</link>\n"
                rss_content += f"        <description>{post['metadata']['description']}</description>\n"
                rss_content += f"        <pubDate>{post['metadata']['updated_datetime'].strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate>\n"
                rss_content += f"        <guid>{self.global_variables['domain']}/{post['metadata']['url']}</guid>\n"
                rss_content += f"        <enclosure url=\"{post_image_url}\" type=\"image/jpeg\" />\n"
                rss_content += "    </item>\n"

            rss_content += "</channel>\n"
            rss_content += "</rss>\n"

            rss_path = os.path.join(self.output_web_path, 'rss.xml')
            with open(rss_path, 'w', encoding='utf-8') as f:
                f.write(rss_content)

    def generate_blog(self):
        if os.path.exists(self.output_web_path):
            shutil.rmtree(self.output_web_path)
        os.makedirs(self.output_web_path, exist_ok=True)

        self.sitemaps = []
        self.copy_static_files()
        self.load_posts()
        self.generate_pages()
        self.generate_post_pages()
        self.generate_site_maps()
        self.generate_rss()
        print("Your new version of the blog is available in web/")


@click.command("build")
def build_command():
    if not os.path.isfile('genopen.config'):
        click.echo("Error: 'genopen.config' not found. Make sure you are in a valid Genopen project folder.")
        return

    try:
        generator = MarkdownToBlogGenerator(config_path='genopen.config')
        generator.generate_blog()
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
