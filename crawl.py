from urllib.parse import urlparse
from bs4 import BeautifulSoup

def normalize_url(url):
    parsed_url = urlparse(url)
    
    base_url = parsed_url.netloc + parsed_url.path
    if base_url.endswith("/"):
        final_url = base_url.rstrip("/")
        return final_url
    else:
        return base_url
    
    

def get_h1_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find("h1")
    if h1_tag:
        return h1_tag.get_text()
    else:
        return ""
   

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.main is not None:
        if soup.main.find("p"):
            p_tag = soup.main.p
            if p_tag:
                return p_tag.get_text()
            else:
                return ""
    else:
        p_tag = soup.p
        if p_tag:
            return p_tag.get_text()
        else:
            return ""

   
def get_urls_from_html(html, base_url):
    