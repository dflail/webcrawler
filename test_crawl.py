import unittest
from crawl import normalize_url

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        url = "https://www.boot.dev/blog/path"
        expected = "www.boot.dev/blog/path"
        result = normalize_url(url)
        self.assertEqual(result, expected)

    def test_normalize_url_port(self):
        input_url = "https://boot.dev:8080/path/"
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


    if __name__ == "__main__":
        unittest.main()