import os
import shutil
import markdown
import yaml
from markdown.extensions.toc import TocExtension
from mdx_math import MathExtension
import re
from bs4 import BeautifulSoup


class RichCMSGenerator:
    @classmethod
    def convert_md_to_html(cls, md_content):
        """Convert Markdown content to HTML, with LaTeX support and table of contents."""
        md = markdown.Markdown(extensions=['markdown.extensions.fenced_code', TocExtension(), MathExtension(enable_dollar_delimiter=True)])
        html_content = md.convert(md_content)
        return html_content

    @classmethod
    def read_markdown_file(cls, file_path):
        """Read Markdown content from a file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @classmethod
    def extract_title(cls, md_content):
        """Extract title from Markdown content."""
        match = re.search(r'^#\s*(.+)', md_content, re.MULTILINE)
        if match:
            return match.group(1)
        return "No Title"

    @classmethod
    def extract_metadata_from_yaml(cls, md_content):
        """Extract metadata from YAML front matter in the markdown content."""
        match = re.match(r'^---\s*\n(.+?)\n---', md_content, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1))
        return {}

    @classmethod
    def read_template_file(cls, template_path):
        """Read HTML template content from a file."""
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()

    @classmethod
    def get_relative_root_path(cls, current_path):
        """Get relative root path from the current file path."""
        depth = len(current_path.strip('./').split('/')) - 1
        relative_path = '../' * depth if depth > 0 else './'
        return relative_path.rstrip('/')

    @classmethod
    def organize_articles_by_directory(cls, articles, base_input_path):
        """Organize articles by their directory paths."""
        organized_articles = {}
        for article in articles:
            dir_path = os.path.dirname(os.path.join(base_input_path, article['path']))
            if dir_path not in organized_articles:
                organized_articles[dir_path] = []
            organized_articles[dir_path].append(article)
        return organized_articles

    @classmethod
    def create_toc(cls, articles, current_file_path, base_input_path):
        """Create a Table of Contents (TOC) that mirrors the directory structure."""
        toc = "<ul>"
        organized_articles = cls.organize_articles_by_directory(articles, base_input_path)

        for dir_path, articles in organized_articles.items():
            # Skip adding an entry if the directory name is '.' (root)
            if os.path.basename(dir_path) == '.':
                for article in articles:
                    title = article['title']
                    link = os.path.relpath(article['path'], os.path.dirname(current_file_path))
                    toc += f"<li><a href='{link}'>{title}</a></li>"
            else:
                dir_name = os.path.basename(dir_path)
                toc += f"<li>{dir_name}<ul>"
                for article in articles:
                    title = article['title']
                    link = os.path.relpath(article['path'], os.path.dirname(current_file_path))
                    toc += f"<li><a href='{link}'>{title}</a></li>"
                toc += "</ul></li>"

        toc += "</ul>"
        return toc

    @classmethod
    def write_html_file(cls, html_content, output_path, template, title, toc, relative_root_path, metadata, meta_tag_block_placeholder="%DYNAMIC-META-TAGS-BLOCK%"):
        """Write HTML content to a file with template formatting, replacing arbitrary metadata tags."""
        # Create a meta tag for each metadata key-value pair
        meta_tags = ""
        for key, value in metadata.items():
            meta_tags += f'<meta name="{key}" content="{value}">\n'

        # Replace basic placeholders in the template
        full_content = (template.replace('%BODY%', html_content)
                                .replace('%TITLE%', title)
                                .replace('%TOC%', toc)
                                .replace('%DYNAMIC-META-TAGS-BLOCK%', meta_tags)
                                .replace('%ROOT%', relative_root_path))

    # Scan and replace arbitrary %META:any_string% placeholders
        placeholders = re.findall(r'%META:([^%]+)%', full_content)
        for placeholder in placeholders:
            metadata_value = metadata.get(placeholder, f'Unknown {placeholder}')
            # Convert metadata_value to string if it's not None
            if metadata_value is not None:
                metadata_value = str(metadata_value)
            full_content = full_content.replace(f'%META:{placeholder}%', metadata_value)


        # Include MathJax script
        mathjax_script = """
        <script type="text/javascript" async
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
        </script>
        """
        full_content = full_content.replace('</head>', f'{mathjax_script}</head>')

        # Format the full_content using BeautifulSoup
        soup = BeautifulSoup(full_content, 'html.parser')
        formatted_html = soup.prettify()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(formatted_html)

    @classmethod
    def clear_output_directory(cls, output_directory):
        """Clear the output directory."""
        if os.path.exists(output_directory):
            shutil.rmtree(output_directory)
        os.makedirs(output_directory, exist_ok=True)

    @classmethod
    def process_markdown(cls, directory_path, base_input_path, articles):
        """Process markdown files in a directory to extract content, metadata, and paths."""
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path) and filename.endswith(".md"):
                md_content = cls.read_markdown_file(file_path)

                # Extract metadata
                metadata = cls.extract_metadata_from_yaml(md_content)
                md_content_without_metadata = re.sub(r'^---\s*\n.*?\n---', '', md_content, flags=re.DOTALL)

                title = cls.extract_title(md_content_without_metadata)
                html_content = cls.convert_md_to_html(md_content_without_metadata)

                relative_output_path = os.path.relpath(directory_path, base_input_path).replace(' ', '_')
                output_path = os.path.join(relative_output_path, filename.replace('.md', '.html'))
                article_info = {
                    'title': title,
                    'path': output_path,
                    'html_content': html_content,
                    'metadata': metadata
                }
                articles.append(article_info)
            elif os.path.isdir(file_path):
                cls.process_markdown(file_path, base_input_path, articles)

    @classmethod
    def generate_site(cls, input_directory, output_directory, template_path):
        """Generate the static site from markdown files."""
        articles = []
        cls.process_markdown(input_directory, input_directory, articles)
        for article in articles:
            title = article['title']
            path = article['path']
            content = article['html_content']
            metadata = article['metadata']
            relative_root_path = cls.get_relative_root_path(path)
            # Pass the correct arguments to create_toc
            toc = cls.create_toc(articles, path, input_directory) 
            full_path = os.path.join(output_directory, path)
            cls.write_html_file(content, full_path, template, title, toc, relative_root_path, metadata)


    @classmethod
    def copy_static_directory(cls, source, destination):
        """Copy static files from the source directory to the destination."""
        if os.path.exists(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)

# Main workflow
input_directory = 'md-content'
output_directory = 'html-output'
template_path = 'template.html'
static_directory = 'static'

template = RichCMSGenerator.read_template_file(template_path)
RichCMSGenerator.clear_output_directory(output_directory)
RichCMSGenerator.generate_site(input_directory, output_directory, template)
RichCMSGenerator.copy_static_directory(static_directory, output_directory)
