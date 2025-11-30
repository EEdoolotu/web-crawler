from urllib.parse import urlparse

def normalize_url(url):
    parsed_url = urlparse(url)
    
    base_url = parsed_url.netloc + parsed_url.path
    if base_url.endswith("/"):
        final_url = base_url.rstrip("/")
        return final_url
    else:
        return base_url
    
    