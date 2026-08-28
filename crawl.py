from urllib.parse import urlsplit

def normalize_url(url: str) -> str:
    # url = "https://www.boot.dev/blog/path"
    parsed = urlsplit(url)
    return parsed.netloc + parsed.path
