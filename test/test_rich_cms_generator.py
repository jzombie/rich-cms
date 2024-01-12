import unittest
import os
from unittest.mock import patch, mock_open
from pyfakefs.fake_filesystem_unittest import TestCase
from bs4 import BeautifulSoup

# TODO: Update
from process import RichCMSGenerator

# TODO: Add more tests to verify TOC order and other navigation elements are working as expected (i.e. breadcrumb nav)
# TODO: Add tests to verify string replacements are working as expected
# TODO: Add tests to verify metadata is properly routed to %DYNAMIC-META-TAGS-BLOCK

class TestRichCMSGenerator(TestCase):
    def setUp(self):
        self.setUpPyfakefs()  # Set up the fake filesystem

    def test_create_toc_generates_valid_html(self):
        # Create fake directory structure and files
        self.fs.create_file('/dir/article1.html', contents='Article 1 Content')
        self.fs.create_dir('/dir/subdir')
        self.fs.create_file('/dir/subdir/article2.html', contents='Article 2 Content')
        self.fs.create_dir('/dir/subdir/subsubdir')
        self.fs.create_file('/dir/subdir/subsubdir/article3.html', contents='Article 3 Content')
        self.fs.create_dir('/dir/subdir2')
        self.fs.create_file('/dir/subdir2/article4.html', contents='Article 4 Content')
        self.fs.create_file('/dir/subdir2/article5.html', contents='Article 5 Content')

        # Mock articles setup
        articles = [
            {'directory_path': '/dir', 'path': '/dir/article1.html', 'title': 'Article 1', 'metadata': {'indexable': True}},
            {'directory_path': '/dir/subdir', 'path': '/dir/subdir/article2.html', 'title': 'Article 2', 'metadata': {'indexable': True}},
            {'directory_path': '/dir/subdir/subsubdir', 'path': '/dir/subdir/subsubdir/article3.html', 'title': 'Article 3', 'metadata': {'indexable': True}},
            {'directory_path': '/dir/subdir2', 'path': '/dir/subdir2/article4.html', 'title': 'Article 4', 'metadata': {'indexable': True}},
            {'directory_path': '/dir/subdir2', 'path': '/dir/subdir2/article5.html', 'title': 'Article 5', 'metadata': {'indexable': True}},
        ]
        current_article = {'path': '/dir/article1'}
        base_input_path = "/dir"

       # Generate TOC HTML
        toc_html = RichCMSGenerator.create_toc(articles, current_article, base_input_path)

        self.assertEqual(toc_html, '<ul><li class="directory"><div class="label"><a href="subdir/article2.html">subdir</a></div><ul><li><a href="subdir/article2.html">Article 2</a></li></ul></li><li><ul>  <li class="directory"><div class="label"><a href="subdir/subsubdir/article3.html">subsubdir</a></div><ul><li><a href="subdir/subsubdir/article3.html">Article 3</a></li></ul></li></ul></li><li class="directory"><div class="label"><a href="subdir2/article4.html">subdir2</a></div><ul><li><a href="subdir2/article4.html">Article 4</a></li><li><a href="subdir2/article5.html">Article 5</a></li></ul></li></ul>', "toc_html matches expected string")

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(toc_html, 'html.parser')

        # Validate nested structure of <ul> and <li>
        ul_elements = soup.find_all('ul')
        for ul in ul_elements:
            self.assertTrue(all(child.name == 'li' for child in ul.children if child.name is not None), "All children of <ul> should be <li>")

        # Check for no adjacent <ul> tags
        for ul in ul_elements:
            self.assertFalse(ul.find_next_sibling("ul"), "<ul> tags should not be adjacent")

        # Check opening and closing tags are <ul>
        self.assertEqual(soup.contents[0].name, 'ul', "Opening tag should be <ul>")
        self.assertEqual(soup.contents[-1].name, 'ul', "Closing tag should be <ul>")

    def test_create_toc_links_to_valid_directories(self):
        # Create fake directory structure and files
        self.fs.create_file('/dir/article1.html', contents='Article 1 Content')
        self.fs.create_dir('/dir/subdir')
        self.fs.create_file('/dir/subdir/article2.html', contents='Article 2 Content')
        self.fs.create_dir('/dir/subdir/subsubdir')
        self.fs.create_file('/dir/subdir/subsubdir/article3.html', contents='Article 3 Content')
        self.fs.create_dir('/dir/subdir2')
        self.fs.create_file('/dir/subdir2/article4.html', contents='Article 4 Content')
        self.fs.create_file('/dir/subdir2/article5.html', contents='Article 5 Content')

        # Mock articles setup
        articles = [
            {'directory_path': '/dir', 'path': '/dir/article1.html', 'title': 'Article 1', 'metadata': {'indexable': True}},
            {'directory_path': '/dir/subdir', 'path': '/dir/subdir/article2.html', 'title': 'Article 2', 'metadata': {'indexable': True}},
            {'directory_path': '/dir/subdir/subsubdir', 'path': '/dir/subdir/subsubdir/article3.html', 'title': 'Article 3', 'metadata': {'indexable': True}},
            {'directory_path': '/dir/subdir2', 'path': '/dir/subdir2/article4.html', 'title': 'Article 4', 'metadata': {'indexable': True}},
            {'directory_path': '/dir/subdir2', 'path': '/dir/subdir2/article5.html', 'title': 'Article 5', 'metadata': {'indexable': True}},
        ]
        current_article = {'path': '/dir/article1'}
        base_input_path = "/dir"

       # Generate TOC HTML
        toc_html = RichCMSGenerator.create_toc(articles, current_article, base_input_path)

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(toc_html, 'html.parser')

        # Validate the directory links in the TOC
        directory_li_elements = soup.find_all('li', class_='directory')
        self.assertTrue(len(directory_li_elements) > 0, "There should be directory list items in the TOC")

        for li in directory_li_elements:
            directory_link = li.find('a')
            self.assertIsNotNone(directory_link, "Each directory list item should contain a link")
            href = directory_link['href']
            dir_label = directory_link.get_text(strip=True)

            # Expected links based on the directory structure
            expected_links = {
                'subdir': 'subdir/article2.html',
                'subsubdir': 'subdir/subsubdir/article3.html',
                'subdir2': 'subdir2/article4.html'
            }

            # Check if the href matches the expected link for the directory
            self.assertTrue(href == expected_links.get(dir_label), 
                            f"Link for '{dir_label}' should point to '{expected_links.get(dir_label)}', but points to '{href}' instead")


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
        """Test reading Markdown content from a file."""
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
                "<p>...all for $65.00 a month. In a smaller city, or a more sparsely settled part of New York city, the same apartment could be had for as low as $20.00 a month.</p>"
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
