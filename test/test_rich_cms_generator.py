import unittest
import sys
import os
from bs4 import BeautifulSoup

# TODO: Update
from process import RichCMSGenerator

class TestRichCMSGenerator(unittest.TestCase):

    def test_convert_md_to_html(self):
        """Test conversion of Markdown to HTML."""
        md_content = "# Test\nThis is a *test*."
        html_content = RichCMSGenerator.convert_md_to_html(md_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        h1_tag = soup.find('h1')
        self.assertIsNotNone(h1_tag)
        self.assertEqual(h1_tag.get_text(), 'Test')

        em_tag = soup.find('em')
        self.assertIsNotNone(em_tag)
        self.assertEqual(em_tag.get_text(), 'test')

    def test_extract_title(self):
        """Test extracting title from Markdown content."""
        md_content = "# My Title\nContent here."
        title = RichCMSGenerator.extract_title(md_content)
        self.assertEqual(title, "My Title")

    def test_extract_metadata_from_yaml(self):
        """Test extracting YAML metadata from Markdown content."""
        md_content = "---\ntitle: Test Page\n---\nContent here."
        metadata = RichCMSGenerator.extract_metadata_from_yaml(md_content)
        self.assertEqual(metadata, {"title": "Test Page"})

    # Additional tests for other methods can be added here

if __name__ == '__main__':
    unittest.main()
