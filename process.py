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
from natsort import natsorted
from markdown.extensions.toc import TocExtension
from mdx_math import MathExtension
from bs4 import BeautifulSoup
import bleach
from urllib.parse import urlparse
import fnmatch

import warnings

class RichCMSGenerator:
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
            dir_path = os.path.dirname(os.path.join(base_input_path, article['path']))
            if dir_path not in organized_articles:
                organized_articles[dir_path] = []

            # Append article directly without changing its structure
            organized_articles[dir_path].append(article)

        # Sort the articles within each directory
        for dir_path, dir_articles in organized_articles.items():
            # First, sort all articles by title using natsorted for natural ordering
            sorted_articles = natsorted(dir_articles, key=lambda x: x['title'].lower())

            # Separate index.md files and other files
            index_md_articles = [article for article in sorted_articles if os.path.basename(article['md_file_path']) == 'index.md']
            non_index_md_articles = [article for article in sorted_articles if os.path.basename(article['md_file_path']) != 'index.md']

            # Concatenate the lists, placing index.md files at the top
            organized_articles[dir_path] = index_md_articles + non_index_md_articles

        return organized_articles

    @classmethod
    def create_toc(cls, articles, current_file_path, base_input_path):
        toc = '<ul>'
        stack = []

        # Normalize the base_input_path for comparison purposes
        normalized_base_input_path = os.path.normpath(base_input_path) + os.path.sep

        # Organize articles by directory for structured TOC generation
        organized_articles = cls.organize_articles_by_directory(
            articles, base_input_path)

        # Normalize the current file path to be relative to base_input_path.
        normalized_current_path = os.path.normpath(
            os.path.join(base_input_path, current_file_path))

        # Loop through each directory and its articles
        for dir_path, articles_in_dir in organized_articles.items():
            normalized_dir_path = os.path.normpath(dir_path) + os.path.sep

            # Determine the relative directory path excluding base_input_path
            relative_dir_path = normalized_dir_path[len(normalized_base_input_path):]

            # Split into breadcrumbs and determine depth
            dir_breadcrumbs = relative_dir_path.strip(os.path.sep).split(os.path.sep)
            dir_depth = len(dir_breadcrumbs) if relative_dir_path else 0

            # Close tags for higher or equal level directories
            while stack and len(stack) > dir_depth:
                toc += "</ul></li>"
                stack.pop()

            # Open tags for new deeper directories
            while len(stack) < dir_depth:
                breadcrumb = dir_breadcrumbs[len(stack)]
                if breadcrumb and not breadcrumb.startswith('.'):
                    toc += f"<li>{breadcrumb}<ul>"
                    stack.append(breadcrumb)
                else:
                    # Skip creating a sublist for directories starting with a dot
                    stack.append(breadcrumb)  # Still need to maintain stack depth

            # Add articles to the TOC
            for article in articles_in_dir:
                rel_path = article['path']
                link = os.path.relpath(rel_path, os.path.dirname(current_file_path))
                title = article['title']
                normalized_article_path = os.path.normpath(
                    os.path.join(base_input_path, rel_path))
                active_class = ' class="active"' if normalized_article_path == normalized_current_path else ''
                toc += f"<li{active_class}><a href='{link}'>{title}</a></li>"

        # Close any remaining open tags to ensure valid HTML structure.
        while stack:
            toc += "</ul></li>"
            stack.pop()
        toc += "</ul>"
        return toc

    @classmethod
    def write_html_file(cls, html_content, output_path, template, title, toc, relative_root_path, metadata, prev_link, next_link, breadcrumb_nav):
        sanitized_title = cls.sanitize_string(title)
        sanitized_metadata = {key: cls.sanitize_string(str(value)) for key, value in metadata.items()}

        # Get the current datetime in UTC
        current_datetime_utc = datetime.datetime.now(pytz.utc)
        gmt_timezone = pytz.timezone('GMT')
        current_datetime_gmt = current_datetime_utc.astimezone(gmt_timezone)
        formatted_datetime = current_datetime_gmt.strftime("%Y-%m-%d %H:%M:%S %z")

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
                path_parts = output_path.split(os.path.sep)
                # TODO: Use pydantic here
                article_info = {
                    'title': title,
                    'path': output_path,
                    'path_parts': path_parts,
                    'md_file_path': file_path,
                    'html_content': html_content,
                    'metadata': metadata
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
    def generate_site(cls, input_directory, output_directory, template_directory):
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
            toc = cls.create_toc(flattened_ordered_articles, path, input_directory)
            prev_link, next_link = cls.generate_navigation_links(path, flattened_ordered_articles, index)
            full_path = os.path.join(output_directory, path)

            breadcrumb_nav = cls.generate_breadcrumb_nav(article, flattened_ordered_articles)

            cls.write_html_file(content, full_path, template, title, toc, relative_root_path, metadata, prev_link, next_link, breadcrumb_nav)

        # Copy template to output
        cls.copy_directory_contents(template_directory, output_directory, exclude_patterns=["template.html"])

        # Copy non-markdown files to output
        cls.copy_directory_contents(input_directory, output_directory, exclude_patterns=["*.md"])

    # TODO: Fix home link (and extract functionality for determining home link into a separate file)
    # TODO: Implement "find_first_article_filename" in TOC for directories
    # TODO: Fix '.' directories when in root files
    @classmethod
    def generate_breadcrumb_nav(cls, article, organized_articles):
        breadcrumbs = []
        path_parts = article['path_parts']

        # Calculate the relative path back to the root
        depth = len(path_parts) - 1  # Number of directories to go up to the root

        # If the first part of the path is '.', set root_path to './', otherwise calculate normally
        root_path = './' if path_parts[0] == '.' else "../" * depth if depth > 0 else ""

        # Home link - point to the first article in the root directory
        root_article_filename = cls.find_first_article_filename('.', organized_articles)
        home_link = f'{root_article_filename}' if root_article_filename else 'index.html'
        breadcrumbs.append(f'<a href="{root_path}{home_link}">Home</a>')


        # Build the breadcrumb path for each part
        for i in range(1, len(path_parts)):
            breadcrumb_segment = '/'.join(path_parts[:i])
            breadcrumb_name = path_parts[i - 1]

            # Skip adding breadcrumb for current directory ('.')
            if breadcrumb_name == '.':
                continue

            # Find the first article's filename in the directory
            dir_path = os.path.join(*path_parts[:i])
            first_article_filename = cls.find_first_article_filename(dir_path, organized_articles)

            # Construct the link to the first article in the directory
            breadcrumb_link = f'<a href="{root_path}{breadcrumb_segment}/{first_article_filename}">{breadcrumb_name}</a>'
            breadcrumbs.append(breadcrumb_link)

        # Note: This is intentionally not in the previous range loop
        breadcrumbs.append(article['title'])

        # Join the breadcrumbs with the separator
        breadcrumb_nav = ' &gt; '.join(breadcrumbs)
        return breadcrumb_nav

    @classmethod
    def find_first_article_filename(cls, dir_path, articles):
        # Normalize the directory path for consistent matching
        normalized_dir_path = os.path.normpath(dir_path)

        # Iterate through the articles list
        for article in articles:
            article_dir_path = os.path.normpath(os.path.dirname(article['path']))

            if article_dir_path == normalized_dir_path:
                # Return the filename of the first article in the directory
                return os.path.basename(article['path'])
        
        # If no articles found in the directory, return an empty string
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
output_directory = 'docs'
template_directory = 'template'

RichCMSGenerator.clear_output_directory(output_directory)
RichCMSGenerator.generate_site(input_directory, output_directory, template_directory)
