from bs4 import BeautifulSoup, Tag
from urllib.parse import urlsplit, SplitResult

def normalize_url(url: str) -> str:
    parsed = urlsplit(url)
    host = strip_default_port(parsed).lower()
    path = parsed.path.rstrip("/")
    return f"{host}{path}"

# temporary stub for the get_heading_from_html function
def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h_tag = soup.find(["h1", "h2", "h3", "h4", "h5", "h6"])
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""

# temporary stub for the get_first_paragraph_from_html function
def get_first_paragraph_from_html(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    main_section = soup.find("main")
    first_p = main_section.find("p") if isinstance(main_section, Tag) else soup.find("p")
    return first_p.get_text(strip=True) if isinstance(first_p, Tag) else ""

def strip_default_port(parsed: SplitResult) -> str:
    netloc = parsed.netloc
    if parsed.scheme == "http" and netloc.endswith(":80"):
        return netloc[:-3]
    if parsed.scheme == "https" and netloc.endswith(":443"):
        return netloc[:-4]
    return netloc
