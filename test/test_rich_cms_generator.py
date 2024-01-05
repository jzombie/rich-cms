import unittest
from unittest.mock import patch, mock_open
from bs4 import BeautifulSoup

# TODO: Update
from process import RichCMSGenerator

# TODO: Add more tests to verify TOC order and other navigation elements are working as expected (i.e. breadcrumb nav)
# TODO: Add tests to verify string replacements are working as expected
# TODO: Add tests to verify metadata is properly routed to %DYNAMIC-META-TAGS-BLOCK

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

    @patch("builtins.open", new_callable=mock_open, read_data="# Test Markdown\nThis is test content.")
    def test_read_markdown_file(self, mock_file):
        """Test reading markdown content from a file."""
        expected_content = "# Test Markdown\nThis is test content."
        read_content = RichCMSGenerator.read_markdown_file('test.md')
        mock_file.assert_called_once_with('test.md', 'r', encoding='utf-8')
        self.assertEqual(read_content, expected_content)

    @patch("os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_write_html_file(self, mock_file, mock_makedirs):
        """Test writing HTML content to a file."""
        RichCMSGenerator.write_html_file(
            "<p>Test Content</p>", 
            "output/test.html", 
            "<html><head></head><body>%BODY%</body></html>", 
            "Test Title", 
            "", 
            ".", 
            {}, 
            "", 
            "", 
            ""
        )
        mock_file.assert_called_once_with("output/test.html", 'w', encoding='utf-8')
        mock_makedirs.assert_called_once_with("output", exist_ok=True)
        file_handle = mock_file()
        file_handle.write.assert_called_once()

    def test_markdown_dollar_sign_handling(self):
        """Test handling of dollar signs in different scenarios."""

        # Temporarily increase maxDiff to view the difference
        original_max_diff = self.maxDiff
        self.maxDiff = 1024

        scenarios = [
            # Simple math equation
            (
                'This is a simple equation: $E=mc^2$.',
                '<p>This is a simple equation: <script type="math/tex">E=mc^2</script>.</p>'
            ),
            # Complex math equation
            (
                "And here's a more complex equation:\n\n$$\n\\frac{d}{dx}\\left( \\int_{a}^{x} f(u)\,du \\right) = f(x)\n$$",
                '<p>And here\'s a more complex equation:</p>\n<p>\n<script type="math/tex; mode=display">\n\\frac{d}{dx}\\left( \\int_{a}^{x} f(u)\,du \\right) = f(x)\n</script>\n</p>'
            ),
            # Regular string with dollar sign for pricing
            (
                "...all for $65.00 a month. In a smaller city, or a more sparsely settled part of New York city, the same apartment could be had for as low as $20.00 a month.",
                "<p>...all for \\$65.00 a month. In a smaller city, or a more sparsely settled part of New York city, the same apartment could be had for as low as \\$20.00 a month.</p>"
            ),
            # Regular string with dollar signs used figuratively
            (
                "...make lots of $$ . Everybody likes to.",
                "<p>...make lots of $$ . Everybody likes to.</p>"
            )
        ]

        for md_content, expected_output in scenarios:
            with self.subTest(md_content=md_content):
                html_content = RichCMSGenerator.convert_md_to_html(md_content)
                self.assertEqual(html_content, expected_output)

        # Decrease the max diff back to the original value
        self.maxDiff = original_max_diff

    # Additional tests for other methods can be added here

if __name__ == '__main__':
    unittest.main()
