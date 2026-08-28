from urllib.parse import urlsplit, SplitResult

def normalize_url(url: str) -> str:
    parsed = urlsplit(url)
    host = strip_default_port(parsed).lower()
    path = parsed.path.rstrip("/")
    return f"{host}{path}"

def strip_default_port(parsed: SplitResult) -> str:
    if (parsed.scheme == "http" and parsed.port == 80) or \
       (parsed.scheme == "https" and parsed.port == 443):
        return parsed.hostname or ""
    return parsed.netloc
