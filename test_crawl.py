import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, extract_page_data

# uv run -m unittest
class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        url = "https://www.boot.dev/blog/path"
        expected = "www.boot.dev/blog/path"
        result = normalize_url(url)
        self.assertEqual(result, expected)

    def test_normalize_http_url_port(self):
        input_url = "http://boot.dev:80/path/"
        actual = normalize_url(input_url)
        expected = "boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_https_url_port(self):
            input_url = "https://boot.dev:443/path/"
            actual = normalize_url(input_url)
            expected = "boot.dev/path"
            self.assertEqual(actual, expected)

    def test_normalize_url_trailing_slash(self):
        input_url = "https://boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_capitals(self):
        input_url = "https://BOOT.DEV/path"
        actual = normalize_url(input_url)
        expected = "boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_root_slash(self):
        input_url = "https://boot.dev/"
        actual = normalize_url(input_url)
        expected = "boot.dev"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic(self) -> None:
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2_fallback(self) -> None:
        input_body = "<html><body><h2>Fallback Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Fallback Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_whitespace(self) -> None:
        input_body = "<html><body><h1>   Whitespace Title   </h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Whitespace Title"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_basic(self) -> None:
        input_body = "<html><body><p>This is the first paragraph.</p></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "This is the first paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self) -> None:
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_paragraph(self) -> None:
        input_body = "<html><body><h1>No paragraphs here</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_headless_page_data(self):
            input_url = "https://crawler-test.com"
            input_body = """<html><body>
                <p>This is the first paragraph.</p>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
            </body></html>"""
            actual = extract_page_data(input_body, input_url)
            expected = {
                "url": "https://crawler-test.com",
                "heading": "",
                "first_paragraph": "This is the first paragraph.",
                "outgoing_links": ["https://crawler-test.com/link1"],
                "image_urls": ["https://crawler-test.com/image1.jpg"],
            }
            self.assertEqual(actual, expected)

    def test_extract_page_data_sans_paragraph(self):
            input_url = "https://crawler-test.com"
            input_body = """<html><body>
                <h1>Test Title</h1>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
            </body></html>"""
            actual = extract_page_data(input_body, input_url)
            expected = {
                "url": "https://crawler-test.com",
                "heading": "Test Title",
                "first_paragraph": "",
                "outgoing_links": ["https://crawler-test.com/link1"],
                "image_urls": ["https://crawler-test.com/image1.jpg"],
            }
            self.assertEqual(actual, expected)

    def test_extract_page_data_without_pictures(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    if __name__ == "__main__":
        unittest.main()