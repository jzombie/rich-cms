"""
This module contains the RichCMSGenerator class for generating rich content.
"""

import os
import shutil
import re
import markdown
import yaml
from natsort import natsorted
from markdown.extensions.toc import TocExtension
from mdx_math import MathExtension
from bs4 import BeautifulSoup


class RichCMSGenerator:
    @classmethod
    def convert_md_to_html(cls, md_content):
        md = markdown.Markdown(extensions=['markdown.extensions.fenced_code', TocExtension(), MathExtension(enable_dollar_delimiter=True)])
        html_content = md.convert(md_content)
        return html_content

    @classmethod
    def read_markdown_file(cls, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @classmethod
    def extract_title(cls, md_content):
        match = re.search(r'^#\s*(.+)', md_content, re.MULTILINE)
        if match:
            return match.group(1)
        return "No Title"

    @classmethod
    def extract_metadata_from_yaml(cls, md_content):
        match = re.match(r'^---\s*\n(.+?)\n---', md_content, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1))
        return {}

    @classmethod
    def read_template_file(cls, template_path):
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()

    @classmethod
    def get_relative_root_path(cls, current_path):
        depth = len(current_path.strip('./').split('/')) - 1
        relative_path = '../' * depth if depth > 0 else './'
        return relative_path.rstrip('/')

    @classmethod
    def organize_articles_by_directory(cls, articles, base_input_path):
        organized_articles = {}
        for article in articles:
            dir_path = os.path.dirname(os.path.join(base_input_path, article['path']))
            if dir_path not in organized_articles:
                organized_articles[dir_path] = []

            # Append the article with a tuple (title, article) for custom sorting
            organized_articles[dir_path].append((article['title'], article))

        # Sort the articles within each directory alphanumerically by title
        for dir_path, dir_articles in organized_articles.items():
            organized_articles[dir_path] = [article for _, article in natsorted(dir_articles, key=lambda x: x[0].lower())]

        return organized_articles


    @classmethod
    def create_toc(cls, articles, current_file_path, base_input_path):
        toc = "<ul>"
        organized_articles = cls.organize_articles_by_directory(articles, base_input_path)

        for k,v in organized_articles.items():

            for article in v:
                rel_path = article['path']
                dir_name = os.path.dirname(article['path'])
                is_base_dir = dir_name == '.'
                
                dir_breadcrumbs = rel_path.split(os.sep)[:-1]

                link = os.path.relpath(article['path'], os.path.dirname(current_file_path))

                title = article['title']

                if not is_base_dir:
                    for breadcrumb in dir_breadcrumbs:
                        toc += f"<li>{breadcrumb}<ul>"
                
                toc += f"<li><a href='{link}'>{title}</a></li>"

                if not is_base_dir:
                    for breadcrumb in dir_breadcrumbs:
                        toc += f"</li></ul>"

        return toc

    @classmethod
    def write_html_file(cls, html_content, output_path, template, title, toc, relative_root_path, metadata):
        meta_tags = "".join(f'<meta name="{key}" content="{value}">\n' for key, value in metadata.items())
        mathjax_script = """
        <script type="text/javascript" async
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
        </script>
        """
        full_content = template.replace('%BODY%', html_content).replace('%TITLE%', title).replace('%TOC%', toc).replace('%ROOT%', relative_root_path)
        full_content = full_content.replace('%DYNAMIC-META-TAGS-BLOCK%', meta_tags)
        full_content = full_content.replace('</head>', f'{mathjax_script}</head>')
        soup = BeautifulSoup(full_content, 'html.parser')
        formatted_html = soup.prettify()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(formatted_html)

    @classmethod
    def clear_output_directory(cls, output_directory):
        if os.path.exists(output_directory):
            shutil.rmtree(output_directory)
        os.makedirs(output_directory, exist_ok=True)

    @classmethod
    def process_markdown(cls, directory_path, base_input_path, articles):
        items = sorted(os.listdir(directory_path), key=lambda item: item.lower())
        for item in items:
            file_path = os.path.join(directory_path, item)
            if os.path.isfile(file_path) and item.endswith(".md"):
                md_content = cls.read_markdown_file(file_path)
                metadata = cls.extract_metadata_from_yaml(md_content)
                md_content_without_metadata = re.sub(r'^---\s*\n.*?\n---', '', md_content, flags=re.DOTALL)
                title = cls.extract_title(md_content_without_metadata)
                html_content = cls.convert_md_to_html(md_content_without_metadata)
                relative_output_path = os.path.relpath(directory_path, base_input_path).replace(' ', '_')
                output_path = os.path.join(relative_output_path, item.replace('.md', '.html'))
                article_info = {'title': title, 'path': output_path, 'html_content': html_content, 'metadata': metadata}
                articles.append(article_info)
            elif os.path.isdir(file_path):
                cls.process_markdown(file_path, base_input_path, articles)

    @classmethod
    def generate_site(cls, input_directory, output_directory, template_path):
        articles = []
        cls.process_markdown(input_directory, input_directory, articles)
        template = cls.read_template_file(template_path)
        cls.clear_output_directory(output_directory)
        for article in articles:
            title = article['title']
            path = article['path']
            content = article['html_content']
            metadata = article['metadata']
            relative_root_path = cls.get_relative_root_path(path)
            toc = cls.create_toc(articles, path, input_directory)
            full_path = os.path.join(output_directory, path)
            cls.write_html_file(content, full_path, template, title, toc, relative_root_path, metadata)

    @classmethod
    def copy_static_directory(cls, source, destination):
        if os.path.exists(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)

# Main workflow
input_directory = 'md-content'
output_directory = 'html-output'
template_path = 'template.html'
static_directory = 'static'

RichCMSGenerator.clear_output_directory(output_directory)
RichCMSGenerator.generate_site(input_directory, output_directory, template_path)
RichCMSGenerator.copy_static_directory(static_directory, output_directory)
