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
        toc = '<ul class="nav">'
        stack = []

        # Organize articles by directory for structured TOC generation
        organized_articles = cls.organize_articles_by_directory(articles, base_input_path)

        # Normalize the current file path to be relative to base_input_path.
        # This helps in identifying the active article in the TOC.
        normalized_current_path = os.path.normpath(os.path.join(base_input_path, current_file_path))

        # Loop through each directory and its articles
        for _, articles_in_dir in organized_articles.items():
            for article in articles_in_dir:
                rel_path = article['path']

                # Generate links relative to the current file path. This ensures that
                # links in the TOC are correct regardless of the current file's location.
                link = os.path.relpath(rel_path, os.path.dirname(current_file_path))
                title = article['title']

                # Normalize the article path for a consistent format. This normalization
                # is crucial for the correct comparison with the normalized current path.
                normalized_article_path = os.path.normpath(os.path.join(base_input_path, rel_path))

                # Determine if this article is the current one being viewed. If so, add
                # the 'active' class for CSS styling.
                active_class = ' class="active"' if normalized_article_path == normalized_current_path else ''
                toc += f"<li{active_class}><a href='{link}'>{title}</a></li>"

                # Handle directory breadcrumbs to build a hierarchical TOC structure.
                dir_breadcrumbs = [bc for bc in rel_path.split(os.sep)[:-1] if bc != '.']
                i = 0
                while i < len(stack) and i < len(dir_breadcrumbs) and stack[i] == dir_breadcrumbs[i]:
                    i += 1
                while len(stack) > i:
                    toc += "</ul></li>"
                    stack.pop()
                while i < len(dir_breadcrumbs):
                    toc += f"<li>{dir_breadcrumbs[i]}<ul>"
                    stack.append(dir_breadcrumbs[i])
                    i += 1

        # Close any remaining open tags to ensure valid HTML structure.
        while stack:
            toc += "</ul></li>"
            stack.pop()
        toc += "</ul>"
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
            content = cls.add_drop_cap(article['html_content'])
            metadata = article['metadata']
            relative_root_path = cls.get_relative_root_path(path)
            toc = cls.create_toc(articles, path, input_directory)
            full_path = os.path.join(output_directory, path)
            cls.write_html_file(content, full_path, template, title, toc, relative_root_path, metadata)

    @classmethod
    def copy_static_directory(cls, source, destination):
        if os.path.exists(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)

    @classmethod
    def add_drop_cap(cls, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        paragraphs = soup.find_all('p')

        for idx, paragraph in enumerate(paragraphs):
            if idx > 1:
                break

            # Assume paragraph with less than 50 characters is a heading
            if paragraph.text.strip() and len(paragraph.text) >= 50:
                first_letter = paragraph.text[0]

                # Check if the first character is a letter (using a regular expression)
                if first_letter.isalpha():
                    rest_of_text = paragraph.text[1:]

                    # Apply drop cap styling
                    paragraph.clear()  # Clear the contents of the paragraph
                    drop_cap_span = soup.new_tag('span', attrs={'class': 'drop-cap'})
                    drop_cap_span.string = first_letter
                    paragraph.insert(0, drop_cap_span)  # Insert the drop cap at the beginning
                    paragraph.insert(1, rest_of_text)  # Insert the rest of the text

                # Stop iterating
                break

        return str(soup)

# Main workflow
input_directory = 'md-content'
output_directory = 'html-output'
template_path = 'template.html'
static_directory = 'static'

RichCMSGenerator.clear_output_directory(output_directory)
RichCMSGenerator.generate_site(input_directory, output_directory, template_path)
RichCMSGenerator.copy_static_directory(static_directory, output_directory)
