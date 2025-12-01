from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio

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


def get_html(url):
    try:
        r = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    except Exception as e:
        raise Exception(f"something went wrong: {e}")

    if r.status_code >= 400:
        raise ValueError("Failed to process request")

    if "text/html" not in r.headers['content-type']:
        raise ValueError("The content type should be text or html")


    return r.text

def safe_get_html(url):
    try:
        return get_html(url)
    except Exception as e:
        print(f"{e}")
        return None
    

def crawl_page(base_url, current_url=None, page_data=None):
    if page_data is None:
        page_data = {}

    if current_url is None:
        current_url = base_url
    
    parsed_current_url = urlparse(current_url)
    parsed_base_url = urlparse(base_url)
    
    hostname = parsed_current_url.netloc.lower()
    domain = parsed_base_url.netloc.lower()

    if hostname != domain:
        return page_data
    else:
        normal_url = normalize_url(current_url)
        
        if normal_url in page_data:
            return page_data
        else:
            data= safe_get_html(current_url)
            if data is None:
                return page_data
            print(f"Currently crawling: {current_url}")
            extracted_data = extract_page_data(data, current_url)
            page_data[normal_url] = extracted_data

            url_list = get_urls_from_html(data, base_url)
            for url in url_list:
                page_data = crawl_page(base_url, url, page_data)

    return page_data




class AsyncCrawler():
    def __init__(self, base_url):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = 2
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
    
    async def __aenter__(self):
		self.session = aiohttp.ClientSession()
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		await self.session.close()

    async def add_page_visit(self, normalized_url):

        # ... later
        async with self.lock:
            if normalized_url not in self.page_data:
                self.page_data[normalized_url] = None
                return True 
            else:
                return False 

    async def get_html(self, url):
        try:
            async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as resp:
                if resp.status >= 400:
                    print("Failed to process request")
                    return None
                
                if "text/html" not in resp.headers['content-type']:
                    print("The content type should be text or html")
                    return None

                return await resp.text()
            
        except Exception as e:
            print(f"{e}")
            return None

    async def crawl_page(self, current_url):    
        parsed_current_url = urlparse(current_url)
        
        
        hostname = parsed_current_url.netloc.lower()
        

        if hostname != self.base_domain:
            return

        norm_url = normalize_url(current_url)

        is_new = await  self.add_page_visit(norm_url)
        if not is_new:
            return

        async with self.semaphore:
        html = await self.get_html(current_url)
        if html is None:
            return

        page_info = extract_page_data(html, current_url)

        # store page_info safely
        async with self.lock:
            self.page_data[normalized_url] = page_info

        next_urls = get_urls_from_html(html, self.base_url)

    # 5. Spawn tasks for child URLs
        tasks = []
        for next_url in next_urls:
            task = asyncio.create_task(self.crawl_page(next_url))
            tasks.append(task)

        if tasks:
            await asyncio.gather(*tasks)

