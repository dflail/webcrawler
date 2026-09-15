from bs4 import BeautifulSoup, Tag
from typing import TypedDict
from urllib.parse import urljoin, urlsplit, SplitResult

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def extract_page_data(html: str, page_url: str) -> PageData:
    heading = get_heading_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)
    img_urls = get_images_from_html(html, page_url)

    return PageData(
        url=page_url,
        heading=heading,
        first_paragraph=first_paragraph,
        outgoing_links=get_urls_from_html(html, page_url),
        image_urls=img_urls,
    )

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h_tag = soup.find(["h1", "h2", "h3", "h4", "h5", "h6"])
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""

def get_first_paragraph_from_html(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    main_section = soup.find("main")
    first_p = main_section.find("p") if isinstance(main_section, Tag) else soup.find("p")
    return first_p.get_text(strip=True) if isinstance(first_p, Tag) else ""

def get_images_from_html(html: str, base_url: str) -> list[str]:
    image_urls = []
    soup = BeautifulSoup(html, "html.parser")
    images = soup.find_all("img")

    for img in images:
        if not isinstance(img, Tag):
            continue
        src = img.get("src")
        if isinstance(src, str) and src:
            try:
                absolute_url = urljoin(base_url, src)
                image_urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {src}")

    return image_urls

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("http://") or href.startswith("https://"):
            urls.append(href)
        elif href.startswith("/"):
            urls.append(base_url + href)
    return urls

def normalize_url(url: str) -> str:
    parsed = urlsplit(url)
    host = strip_default_port(parsed).lower()
    path = parsed.path.rstrip("/")
    return f"{host}{path}"

def strip_default_port(parsed: SplitResult) -> str:
    netloc = parsed.netloc
    if parsed.scheme == "http" and netloc.endswith(":80"):
        return netloc[:-3]
    if parsed.scheme == "https" and netloc.endswith(":443"):
        return netloc[:-4]
    return netloc
