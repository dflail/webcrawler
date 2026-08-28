import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html

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

    # Function incomplete, so we will just test the stubs for now
    def test_get_heading_from_html(self):
        html = "<html><head><title>Test</title></head><body><h1>Heading</h1></body></html>"
        expected = "Heading"
        result = get_heading_from_html(html)
        self.assertEqual(result, expected)

    # Function incomplete, so we will just test the stubs for now
    def test_get_first_paragraph_from_html(self):
        html = "<html><head><title>Test</title></head><body><p>Paragraph 1</p><p>Paragraph 2</p></body></html>"
        expected = ["Paragraph 1"]
        result = get_first_paragraph_from_html(html)
        self.assertEqual(result, expected)

    if __name__ == "__main__":
        unittest.main()