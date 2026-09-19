from asyncio import gather, Lock, Semaphore
from typing import TypedDict
from urllib.parse import urljoin, urlsplit
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag


class AsyncCrawler:

    def __init__(self, base_url: str, max_concurrency: int = 5):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data: dict[str, PageData] = {}
        self.visited: set[str] = set()
        self.lock = Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = Semaphore(max_concurrency)
        self.session: ClientSession | None = None

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.visited:
                return False
            self.visited.add(normalized_url)
            return True

    async def get_html(self, url: str) -> str:
        if self.session is None:
            raise RuntimeError("Session not initialized. Use 'async with' context.")
        async with self.semaphore:
            async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
                if response.status > 399:
                    raise Exception(f"got HTTP error: {response.status} {response.reason}")
                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    raise Exception(f"got non-HTML response: {content_type}")
                return await response.text()

    async def crawl_page(self, current_url: str | None = None):
        if current_url is None:
            current_url = self.base_url

        normalized_url = normalize_url(current_url)
        if not await self.add_page_visit(normalized_url):
            return

        try:
            html = await self.get_html(current_url)
            print(f"Crawling: {current_url}")
        except Exception as e:
            print(f"Error fetching {current_url}: {e}")
            return

        page_info = extract_page_data(html, current_url)
        self.page_data[normalized_url] = page_info

        tasks = []
        for link in page_info["outgoing_links"]:
            if urlsplit(link).netloc == self.base_domain:
                tasks.append(self.crawl_page(link))

        await gather(*tasks)

    async def crawl(self):
        await self.crawl_page()
        return self.page_data

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

async def crawl_site_async(base_url: str) -> dict[str, PageData]:
    async with AsyncCrawler(base_url) as crawler:
        return await crawler.crawl()

# def crawl_page(
#         base_url: str,
#         current_url: str | None=None,
#         page_data: dict[str, PageData] | None = None
#     ) -> dict[str, PageData]:

#     if current_url is None:
#         current_url = base_url

#     if page_data is None:
#         page_data = {}
        
#     if urlsplit(base_url).netloc == urlsplit(current_url).netloc:
#         normalized_url = normalize_url(current_url)
#         if normalized_url in page_data:
#             return page_data
#         try:
#             html = get_html(current_url)
#             print(f"Crawling: {current_url}")
#         except Exception as e:
#             print(f"Error fetching {current_url}: {e}")
#             return page_data
        

#         page_info = extract_page_data(html, current_url)
#         page_data[normalized_url] = page_info

#         for link in page_info["outgoing_links"]:
#             crawl_page(base_url, link, page_data)

#         return page_data
#     else:
#         return page_data

def normalize_url(url: str) -> str:
    parsed_url = urlsplit(url)
    full_path = f"{parsed_url.netloc}{parsed_url.path}"
    full_path = full_path.rstrip("/")
    return full_path.lower()


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h_tag = soup.find("h1") or soup.find("h2")
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    main_section = soup.find("main")
    if isinstance(main_section, Tag):
        first_p = main_section.find("p")
    else:
        first_p = soup.find("p")

    return first_p.get_text(strip=True) if isinstance(first_p, Tag) else ""


def get_urls_from_html(html: str, base_url: str) -> list[str]:
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all("a")

    for anchor in anchors:
        if not isinstance(anchor, Tag):
            continue
        href = anchor.get("href")
        if isinstance(href, str) and href:
            try:
                absolute_url = urljoin(base_url, href)
                urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {href}")

    return urls


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


def extract_page_data(html: str, page_url: str) -> PageData:
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }


# def get_html(url: str) -> str:
#     try:
#         response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
#     except Exception as e:
#         raise Exception(f"network error while fetching {url}: {e}")

#     if response.status_code > 399:
#         raise Exception(f"got HTTP error: {response.status_code} {response.reason}")

#     content_type = response.headers.get("content-type", "")
#     if "text/html" not in content_type:
#         raise Exception(f"got non-HTML response: {content_type}")

#     return response.text
