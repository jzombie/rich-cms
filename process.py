import os
import shutil
import markdown
import yaml
import datetime
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
import re

def convert_md_to_html(md_content):
    """Convert Markdown content to HTML, with syntax highlighting for code blocks."""
    return markdown.markdown(md_content, extensions=[FencedCodeExtension(), CodeHiliteExtension(pygments_style='friendly', linenums=False)])

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_title(md_content):
    match = re.search(r'^#\s*(.+)', md_content, re.MULTILINE)
    if match:
        return match.group(1)
    return "No Title"

def extract_metadata_from_yaml(md_content):
    """Extract metadata from YAML front matter in the markdown content."""
    match = re.match(r'^---\s*\n(.+?)\n---', md_content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return {}

def read_template_file(template_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_relative_root_path(current_path):
    depth = len(current_path.strip('./').split('/')) - 1
    relative_path = '../' * depth if depth > 0 else './'
    return relative_path.rstrip('/')

def create_toc(articles, relative_root_path):
    toc = "<ul>"
    parent_paths = set()
    for title, path, _, _ in articles:
        parent_path = os.path.dirname(path)
        if parent_path not in parent_paths:
            parent_name = os.path.basename(parent_path).strip().replace('_', ' ')
            if parent_name != ".":
                toc += f"<li>{parent_name}<ul>"
            parent_paths.add(parent_path)
        link = os.path.join(relative_root_path, path.lstrip('./'))
        toc += f"<li><a href='{link}'>{title}</a></li>"
    toc += "</ul>" * len(parent_paths)
    toc += "</ul>"
    return toc

def write_html_file(html_content, output_path, template, title, toc, relative_root_path, metadata):
    # Replace basic placeholders in the template
    full_content = (template.replace('%BODY%', html_content)
                            .replace('%TITLE%', title)
                            .replace('%TOC%', toc)
                            .replace('%ROOT%', relative_root_path))

    # Replace META placeholders with corresponding metadata
    for key, value in metadata.items():
        meta_placeholder = f'%META:{key}%'
        full_content = full_content.replace(meta_placeholder, str(value))

    # Remove any unused META placeholders
    full_content = re.sub(r'%META:.*?%', '', full_content)

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
            metadata = extract_metadata_from_yaml(md_content)
            html_content = convert_md_to_html(md_content)
            relative_output_path = os.path.relpath(directory_path, base_input_path).replace(' ', '_')
            output_path = os.path.join(relative_output_path, filename.replace('.md', '.html'))
            articles.append((title, output_path, html_content, metadata))
        elif os.path.isdir(file_path):
            process_markdown(file_path, base_input_path, articles)

def generate_site(input_directory, output_directory, template_path):
    articles = []
    process_markdown(input_directory, input_directory, articles)
    for title, path, content, metadata in articles:
        relative_root_path = get_relative_root_path(path)
        toc = create_toc(articles, relative_root_path)
        full_path = os.path.join(output_directory, path)
        write_html_file(content, full_path, template, title, toc, relative_root_path, metadata)

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
