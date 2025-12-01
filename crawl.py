from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def normalize_url(url):
    parsed_url = urlparse(url)
    
    base_url = parsed_url.netloc.lower() + parsed_url.path
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
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find_all("a")
    urls = []

    for link in all_links:
        href = link.get('href')
        if href:
            urls.append(urljoin(base_url, href))
    
    return urls

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    all_images = soup.find_all("img")
    image_list = []

    for image in all_images:
         src = image.get("src")
         if src:
            image_list.append(urljoin(base_url, src))

    return image_list

def extract_page_data(html, page_url):
    expected = {
            "url": page_url,
            "h1": get_h1_from_html(html),
            "first_paragraph": get_first_paragraph_from_html(html),
            "outgoing_links": get_urls_from_html(html, page_url),
            "image_urls": get_images_from_html(html, page_url),
        }
    return expected

