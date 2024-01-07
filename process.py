"""
This module contains the RichCMSGenerator class for generating rich content.
"""

import os
import shutil
import re
import datetime
import pytz
import markdown
import yaml
import urllib.parse
import xml.etree.ElementTree as ET
import xml.dom.minidom
import warnings
import bleach
import fnmatch
from natsort import natsorted, natsort_keygen
from markdown.extensions.toc import TocExtension
from mdx_math import MathExtension
from bs4 import BeautifulSoup, Comment
from urllib.parse import urlparse

class RichCMSGenerator:
    total_word_count = 0

    @staticmethod
    def calculate_word_count(text):
        """
        Calculates the number of words in the given text.
        """
        words = text.split()
        return len(words)
    
    @staticmethod
    def calculate_reading_time(word_count):
        """
        Calculates the estimated reading time based on the word count.
        Average reading speed is considered 200 words per minute.
        """
        reading_speed_per_minute = 200
        return max(1, round(word_count / reading_speed_per_minute))

    @staticmethod
    def sanitize_string(input_string):
        """
        Sanitizes the input string using the bleach library.
        """
        sanitized_string = bleach.clean(input_string, strip=True)
        return sanitized_string

    @classmethod
    def convert_md_to_html(cls, md_content):
        # Escape dollar signs that are likely part of monetary values
        # This regex targets a dollar sign followed by a number, optionally with a decimal part
        escaped_md_content = re.sub(r'(?<!\\)\$(\d+(\.\d+)?)', r'\\\$\1', md_content)
        
        # Convert Markdown to HTML
        md = markdown.Markdown(extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            TocExtension(),
            MathExtension(enable_dollar_delimiter=True),
            'markdown.extensions.extra'
        ])
        html_content = md.convert(escaped_md_content)

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Suppress MarkupResemblesLocatorWarning
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, message="The input looks more like a filename than markup.")

            # Convert URLs in text nodes to clickable links using bleach
            for text_node in soup.find_all(string=True):
                if text_node.parent.name not in ['a', 'script', 'style']:
                    linked_text = bleach.linkify(str(text_node))
                    new_node = BeautifulSoup(linked_text, 'html.parser')
                    text_node.replace_with(new_node)

            # Convert URLs in text nodes to clickable links using bleach
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                parsed_href = urlparse(href)
                if not parsed_href.netloc:
                    # Do nothing if it's a relative link
                    continue
                # Add target="_blank" to non-relative links
                a_tag['target'] = '_blank'
                # Add rel="noopener noreferrer" to non-relative links
                a_tag['rel'] = 'noopener noreferrer'

        # Convert soup back to string
        return str(soup)


    @classmethod
    def read_markdown_file(cls, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @classmethod
    def extract_title(cls, md_content):
        sanitized_md_content = cls.sanitize_string(md_content)
        match = re.search(r'^#\s*(.+)', sanitized_md_content, re.MULTILINE)
        if match:
            return match.group(1)
        return "No Title"

    @classmethod
    def extract_metadata_from_yaml(cls, md_content):
        sanitized_md_content = cls.sanitize_string(md_content)
        match = re.match(r'^---\s*\n(.+?)\n---', sanitized_md_content, re.DOTALL)
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
            article_dir_path = os.path.dirname(article['path'])
            rel_dir_path = os.path.relpath(article_dir_path, base_input_path)
            rel_dir_path = '.' if rel_dir_path == '' else rel_dir_path

            # Check if the article is an index.html and update metadata if needed
            if os.path.basename(article['path']).lower() == 'index.html':
                article['metadata'].setdefault('sort_priority', 1000)

            if rel_dir_path not in organized_articles:
                organized_articles[rel_dir_path] = []

            organized_articles[rel_dir_path].append(article)

        # Create a natsort key generator
        natsort_key = natsort_keygen()

        # Sort articles within each directory
        for dir_path, articles_list in organized_articles.items():
            organized_articles[dir_path] = sorted(
                articles_list, 
                key=lambda x: (
                    -x['metadata'].get('sort_priority', 0),
                    natsort_key(os.path.basename(x['path']))
                )
            )

        # Use natsort for sorting directories
        sorted_organized_articles = natsorted(organized_articles.items(), key=lambda x: x[0])

        return dict(sorted_organized_articles)

    @classmethod
    def create_toc(cls, articles, current_article, base_input_path):
        # Filtering out non-indexable articles
        indexable_articles = [article for article in articles if article['metadata'].get('indexable', True)]
        organized_articles = cls.organize_articles_by_directory(indexable_articles, base_input_path)
        current_article_path = os.path.normpath(current_article['path'])

        def create_sub_toc(dir_path, indent_level=0):
            toc_sub = '<ul>'
            for subdir, subdir_articles in organized_articles.items():
                # This condition checks if the current subdirectory is directly under the directory we are currently processing.
                # os.path.normpath() is used to normalize the path by collapsing redundant separators and up-level references.
                # os.path.dirname(subdir) gets the parent directory of the current 'subdir'.
                # If the parent directory of 'subdir' is not the same as the 'dir_path' we are currently processing,
                # it means 'subdir' is not a direct child of 'dir_path' but rather a subdirectory in a different branch of the directory tree.
                # In such a case, the loop skips this 'subdir' and continues with the next one.
                if os.path.normpath(os.path.dirname(subdir)) != os.path.normpath(dir_path):
                    continue

                dir_label = os.path.basename(subdir) if subdir != '..' else 'Home'

                is_current_dir = os.path.normpath(current_article_path).startswith(os.path.normpath(os.path.join(base_input_path, subdir)))

                first_article_filename = cls.find_first_article_filename(
                    os.path.abspath(
                        os.path.join(
                            base_input_path,
                            os.path.normpath(
                                os.path.join(
                                    base_input_path,
                                    subdir
                                )
                            )
                        )
                    ),
                    articles
                )
                first_article_link = os.path.relpath(
                    os.path.join(
                        os.path.normpath(
                            os.path.join(
                                base_input_path, subdir
                            )
                        ),
                        first_article_filename
                    ),
                    os.path.dirname(current_article_path)
                )

                active_class = ' active-dir' if is_current_dir else ''

                if subdir != '..':
                    toc_sub += '  ' * indent_level + f'<li class="directory {active_class}"><div class="label"><a href="{first_article_link}">{dir_label}</a></div>'
                else:
                    toc_sub += '  ' * indent_level + f'<li>'

                # Add articles in this directory
                toc_sub += '<ul>'
                for article in subdir_articles:
                    article_path = article['path']

                    relative_path = os.path.relpath(article_path, os.path.dirname(current_article_path))
                    is_current_article = os.path.normpath(current_article_path) == os.path.normpath(article_path)
                    active_article_class = ' class="active"' if is_current_article else ''
                    toc_sub += f'<li{active_article_class}><a href="{relative_path}">{article["title"]}</a></li>'

                toc_sub += '</ul>'

                toc_sub += '</li>'

                # If there are subdirectories, handle them recursively inside the current directory's <li>
                if any(os.path.normpath(os.path.dirname(sub)) == os.path.normpath(subdir) for sub in organized_articles.keys()):
                    toc_sub += '<li>'
                    toc_sub += create_sub_toc(subdir, indent_level + 1)
                    toc_sub += '</li>'

            toc_sub += '</ul>'
            return toc_sub

        return create_sub_toc('.')




    @classmethod
    def write_html_file(cls, html_content, output_path, template, title, toc, relative_root_path, metadata, prev_link, next_link, breadcrumb_nav):
        sanitized_title = cls.sanitize_string(title)
        sanitized_metadata = {key: cls.sanitize_string(str(value)) for key, value in metadata.items()}

        # Get the current datetime in UTC
        current_datetime_utc = datetime.datetime.now(pytz.utc)
        gmt_timezone = pytz.timezone('GMT')
        current_datetime_gmt = current_datetime_utc.astimezone(gmt_timezone)
        formatted_datetime = current_datetime_gmt.strftime("%Y-%m-%d %H:%M:%S %z")
        reading_time = cls.calculate_reading_time(metadata.get('word_count', 0))

        meta_tags = "".join(f'<meta name="{key}" content="{value}">\n' for key, value in sanitized_metadata.items())
        mathjax_script = """
        <script type="text/javascript" async
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
        </script>
        """
        full_content = template.replace('%BODY%', html_content).replace('%TITLE%', sanitized_title).replace('%TOC%', toc).replace('%ROOT%', relative_root_path)
        full_content = full_content.replace('%DYNAMIC-META-TAGS-BLOCK%', meta_tags)
        full_content = full_content.replace('</head>', f'{mathjax_script}</head>')
        full_content = full_content.replace('%PREV_LINK%', prev_link).replace('%NEXT_LINK%', next_link)
        full_content = full_content.replace('%BREADCRUMB_NAV%', breadcrumb_nav)
        full_content = full_content.replace('%BUILD_DATETIME%', formatted_datetime)
        full_content = full_content.replace('%READING_TIME%', f"{reading_time}")


        soup = BeautifulSoup(full_content, 'html.parser')

        # Remove HTML comments
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

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
                word_count = cls.calculate_word_count(md_content)
                cls.total_word_count += word_count

                metadata = cls.extract_metadata_from_yaml(md_content)
                metadata['word_count'] = word_count

                md_content_without_metadata = re.sub(r'^---\s*\n.*?\n---', '', md_content, flags=re.DOTALL)
                title = cls.extract_title(md_content_without_metadata)
                html_content = cls.convert_md_to_html(md_content_without_metadata)
                relative_output_path = os.path.relpath(directory_path, base_input_path)
                output_path = os.path.join(relative_output_path, item.replace('.md', '.html'))
                path_parts = output_path.split(os.path.sep)
                # TODO: Use pydantic here
                article_info = {
                    'title': title,
                    'path': output_path,
                    'directory_path': directory_path,
                    'path_parts': path_parts,
                    'md_file_path': file_path,
                    'html_content': html_content,
                    'metadata': metadata,
                }

                articles.append(article_info)
            elif os.path.isdir(file_path):
                cls.process_markdown(file_path, base_input_path, articles)

    @classmethod
    def generate_navigation_links(cls, current_path, flattened_ordered_articles, current_index):
        current_dir = os.path.dirname(current_path)
        navigation_links = {"previous": None, "next": None}

        # Determine the previous and next articles
        if current_index > 0:
            navigation_links["previous"] = flattened_ordered_articles[current_index - 1]
        if current_index < len(flattened_ordered_articles) - 1:
            navigation_links["next"] = flattened_ordered_articles[current_index + 1]

        # Generate the navigation links
        for key, article in navigation_links.items():
            if article:
                article_rel_path = os.path.relpath(article['path'], current_dir)
                link_text = "&laquo; Previous" if key == "previous" else "Next &raquo;"
                navigation_links[key] = f"<a href='{article_rel_path}' class='{key}'>{link_text}</a>"
            else:
                link_text = "&laquo; Previous" if key == "previous" else "Next &raquo;"
                navigation_links[key] = f"<a href='#' class='{key} disabled'>{link_text}</a>"

        return navigation_links["previous"], navigation_links["next"]
    
    @classmethod
    def copy_directory_contents(cls, source_directory, destination_directory, include_patterns=None, exclude_patterns=None):
        """
        Copies files and directories from source_directory to destination_directory
        based on include and exclude wildcard patterns.
        """
        if include_patterns is None:
            include_patterns = ['*']  # By default include everything
        if exclude_patterns is None:
            exclude_patterns = []  # By default exclude nothing

        for item in os.listdir(source_directory):
            source_item = os.path.join(source_directory, item)
            destination_item = os.path.join(destination_directory, item)

            # Check if item matches any of the exclude patterns
            if any(fnmatch.fnmatch(item, pattern) for pattern in exclude_patterns):
                continue

            # Check if item matches any of the include patterns
            if not any(fnmatch.fnmatch(item, pattern) for pattern in include_patterns):
                continue

            if os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item, dirs_exist_ok=True)
            else:
                shutil.copy2(source_item, destination_item)

    @classmethod
    def generate_site(cls, input_directory, output_directory, template_directory, base_url = None):
        articles = []
        cls.process_markdown(input_directory, input_directory, articles)
        template_path = os.path.join(template_directory, 'template.html')
        template = cls.read_template_file(template_path)
        cls.clear_output_directory(output_directory)

        # Organize articles by directory and create a flattened ordered list
        organized_articles = cls.organize_articles_by_directory(articles, input_directory)
        flattened_ordered_articles = [article for dir_articles in organized_articles.values() for article in dir_articles]

        for index, article in enumerate(flattened_ordered_articles):
            title = article['title']
            path = article['path']
            content = cls.add_drop_cap(article['html_content'])
            metadata = article['metadata']
            relative_root_path = cls.get_relative_root_path(path)
            toc = cls.create_toc(flattened_ordered_articles, article, input_directory)
            prev_link, next_link = cls.generate_navigation_links(path, flattened_ordered_articles, index)
            full_path = os.path.join(output_directory, path)

            breadcrumb_nav = cls.generate_breadcrumb_nav(input_directory, article, flattened_ordered_articles)            

            cls.write_html_file(content, full_path, template, title, toc, relative_root_path, metadata, prev_link, next_link, breadcrumb_nav)

        # Copy template to output
        cls.copy_directory_contents(template_directory, output_directory, exclude_patterns=["template.html"])

        # Copy non-markdown files to output
        cls.copy_directory_contents(input_directory, output_directory, exclude_patterns=["*.md"])

        if base_url:
            cls.generate_sitemap(articles, base_url, output_directory)

        # Print the article tree
        cls.print_article_tree(articles, input_directory)

    @classmethod
    def generate_sitemap(cls, articles, base_url, output_directory):
        """
        Generates a formatted sitemap XML for the website with URL encoding and XML declaration.
        """
        urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
        
        for article in articles:
            url = ET.SubElement(urlset, 'url')
            loc = ET.SubElement(url, 'loc')
            # Normalize and encode the URL path
            article_url_path = os.path.normpath(article['path']).replace('\\', '/')
            encoded_article_url_path = urllib.parse.quote(article_url_path, safe='/')
            loc.text = f"{base_url}/{encoded_article_url_path}"
            lastmod = ET.SubElement(url, 'lastmod')
            lastmod.text = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Convert to string and parse using minidom for pretty printing
        rough_string = ET.tostring(urlset, 'utf-8')
        reparsed = xml.dom.minidom.parseString(rough_string)

        # Write the formatted XML to file with XML declaration
        with open(os.path.join(output_directory, 'sitemap.xml'), 'w', encoding='utf-8') as file:
            file.write(reparsed.toprettyxml(indent="\t", newl="\n", encoding="UTF-8").decode('utf-8'))

    # TODO: Extract functionality for determining home link
    @classmethod
    def generate_breadcrumb_nav(cls, input_directory, article, organized_articles):
        breadcrumbs = []
        path_parts = article['path_parts']

        # Calculate the relative path back to the root
        depth = len(path_parts) - 1  # Number of directories to go up to the root
        root_path = './' if path_parts[0] == '.' else "../" * depth if depth > 0 else ""

        # Home link - point to the first article in the root directory
        root_article_filename = cls.find_first_article_filename(os.path.join(input_directory, '.'), organized_articles)
        home_link = f'{root_article_filename}' if root_article_filename else 'index.html'
        breadcrumbs.append(f'<a href="{root_path}{home_link}">Home</a>')

        # Build the breadcrumb path for each part
        for i in range(1, len(path_parts)):
            breadcrumb_segment = '/'.join(path_parts[:i])
            breadcrumb_name = path_parts[i - 1]

            if breadcrumb_name == '.':
                continue

            # Construct the full directory path
            dir_path = os.path.join(input_directory, *path_parts[:i])
            first_article_filename = cls.find_first_article_filename(dir_path, organized_articles)

            # Construct the link to the first article in the directory
            breadcrumb_link = f'<a href="{root_path}{breadcrumb_segment}/{first_article_filename}">{breadcrumb_name}</a>'
            breadcrumbs.append(breadcrumb_link)

        breadcrumbs.append(article['title'])  # Adding the current article's title

        # Join the breadcrumbs with the separator
        breadcrumb_nav = ' &gt; '.join(breadcrumbs)
        return breadcrumb_nav

    @classmethod
    def find_first_article_filename(cls, dir_path, articles):
        dir_path = os.path.abspath(dir_path)

        for article in articles:
            if os.path.abspath(article['directory_path']) == dir_path:
                html_filename = os.path.basename(article['path'])
                return html_filename
        
        return ''



    @classmethod
    def add_drop_cap(cls, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        paragraphs = soup.find_all('p')

        for idx, paragraph in enumerate(paragraphs):
            if idx > 1:
                break

            word_count = len(paragraph.text.strip().split())

            # Assume paragraph with less than 8 words is a heading
            if word_count >= 8:
                first_letter = paragraph.text[0]

                # Check if the first character is a letter (using a regular expression)
                if first_letter.isalpha():
                    # Apply drop cap styling by adding class
                    paragraph['class'] = paragraph.get('class', []) + ['has-drop-cap']

                # Stop iterating
                break

        return str(soup)

    
    @classmethod
    def print_article_tree(cls, articles, base_input_path):
        """
        Prints the tree structure of articles organized by directory.
        """
        organized_articles = cls.organize_articles_by_directory(articles, base_input_path)

        for dir_path in organized_articles.keys():
            depth = dir_path.count(os.sep)
            indent = '    ' * depth
            dir_name = os.path.basename(dir_path) if dir_path != '.' else base_input_path
            print(f"{indent}|--{dir_name}/")
            for article in sorted(organized_articles[dir_path], key=lambda x: x['path']):
                print(f"{indent}|  |--{os.path.basename(article['path'])}")

# Main workflow
input_directory = 'md-content'
output_directory = 'docs'
template_directory = 'template'
base_url = 'https://richcms.zenosmosis.com'  # Replace with your domain

RichCMSGenerator.generate_site(input_directory, output_directory, template_directory, base_url)

print(f"Total word count for the site: {RichCMSGenerator.total_word_count}")
