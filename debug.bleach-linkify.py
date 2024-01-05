from markdown import Markdown
from bs4 import BeautifulSoup
import bleach

# Sample markdown content
markdown_content = """
1. Spotify: https://engineering.atspotify.com/
2. Google: https://blog.research.google/
3. Slack: https://slack.engineering/
"""

# Convert markdown to HTML
md = Markdown(extensions=['extra'])
html_content = md.convert(markdown_content)
print("After markdown conversion:\n", html_content)

# Parse with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
print("After BeautifulSoup parsing:\n", soup.prettify())

# TODO: Debug: Seems that Google and Slack are not properly being turned into links

# Linkify with bleach
# Note: Bleach linkify may not be necessary if URLs are already converted to links by Markdown
linkified_content = bleach.linkify(str(soup))
print("After bleach linkify:\n", linkified_content)
