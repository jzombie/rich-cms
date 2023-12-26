import os
import shutil
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
import re

def convert_md_to_html(md_content):
    """
    Convert Markdown content to HTML, with syntax highlighting for code blocks.
    """
    return markdown.markdown(md_content, extensions=[FencedCodeExtension(), CodeHiliteExtension(pygments_style='friendly', linenums=False)])

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_title(md_content):
    match = re.search(r'^#\s*(.+)', md_content, re.MULTILINE)
    if match:
        return match.group(1)
    return "No Title"

def read_template_file(template_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_relative_root_path(current_path):
    depth = len(current_path.strip('./').split('/')) - 1
    relative_path = '../' * depth if depth > 0 else './'
    # Remove trailing slash if it exists
    return relative_path.rstrip('/')

def create_toc(articles, relative_root_path):
    def get_parent_directory(path):
        # Get the parent directory of a path
        parts = path.split('/')
        if len(parts) > 1:
            return '/'.join(parts[:-1])
        else:
            return None

    toc = "<ul>"
    parent_paths = set()  # To keep track of unique parent paths
    for title, path, _ in articles:
        parent_path = get_parent_directory(path)

        # Skip rendering list items with a title of a single dot "."
        if title.strip() == ".":
            continue

        # Check if this parent path has been added to the TOC
        if parent_path not in parent_paths:
            # Exclude "." when it's the parent directory and replace underscores with spaces
            parent_name = os.path.basename(parent_path).strip().replace('_', ' ')
            if parent_name != ".":
                toc += f"<li>{parent_name}<ul>"
            parent_paths.add(parent_path)
        link = os.path.join(relative_root_path, path.lstrip('./'))
        toc += f"<li><a href='{link}'>{title}</a></li>"
    toc += "</ul>" * len(parent_paths)  # Close all opened <ul> tags
    toc += "</ul>"
    return toc


def write_html_file(html_content, output_path, template, title, toc, relative_root_path):
    full_content = (template.replace('%BODY%', html_content)
                            .replace('%TITLE%', title)  # Display titles with spaces
                            .replace('%TOC%', toc)
                            .replace('%ROOT%', relative_root_path))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(full_content)

def clear_output_directory(output_directory):
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory, exist_ok=True)

def process_markdown(directory_path, base_input_path, articles):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path) and filename.endswith(".md"):
            md_content = read_markdown_file(file_path)
            title = extract_title(md_content)
            html_content = convert_md_to_html(md_content)
            relative_output_path = os.path.relpath(directory_path, base_input_path).replace(' ', '_')
            output_path = os.path.join(relative_output_path, filename.replace('.md', '.html'))
            articles.append((title, output_path, html_content))
        elif os.path.isdir(file_path):
            process_markdown(file_path, base_input_path, articles)

def generate_site(input_directory, output_directory, template_path):
    articles = []
    process_markdown(input_directory, input_directory, articles)
    for title, path, content in articles:
        relative_root_path = get_relative_root_path(path)
        toc = create_toc(articles, relative_root_path)
        full_path = os.path.join(output_directory, path)
        write_html_file(content, full_path, template, title, toc, relative_root_path)

def copy_static_directory(source, destination):
    if os.path.exists(source):
        shutil.copytree(source, destination, dirs_exist_ok=True)

# Main workflow
input_directory = 'md-content'
output_directory = 'html-output'
template_path = 'template.html'
static_directory = 'static'

template = read_template_file(template_path)
clear_output_directory(output_directory)
generate_site(input_directory, output_directory, template)

copy_static_directory(static_directory, output_directory)
