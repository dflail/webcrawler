import unittest
from crawl import normalize_url

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        url = "https://www.boot.dev/blog/path"
        expected = "www.boot.dev/blog/path"
        result = normalize_url(url)
        print(f"Testing normalize_url with input: {url}")
        self.assertEqual(result, expected)

    if __name__ == "__main__":
        unittest.main()