from bs4 import BeautifulSoup, Tag
from urllib.parse import urlsplit, SplitResult

def normalize_url(url: str) -> str:
    parsed = urlsplit(url)
    host = strip_default_port(parsed).lower()
    path = parsed.path.rstrip("/")
    return f"{host}{path}"

# temporary stub for the get_heading_from_html function
def get_heading_from_html(html: str) -> str:
    return ""

# temporary stub for the get_first_paragraph_from_html function
def get_first_paragraph_from_html(html: str) -> list[str]:
    return []

def strip_default_port(parsed: SplitResult) -> str:
    netloc = parsed.netloc
    if parsed.scheme == "http" and netloc.endswith(":80"):
        return netloc[:-3]
    if parsed.scheme == "https" and netloc.endswith(":443"):
        return netloc[:-4]
    return netloc
