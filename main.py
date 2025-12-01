import sys
from crawl import crawl_page

print("Script name:", sys.argv[0]) # example.py


def main():
    print("Hello from web-crawler!")
    

    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    
    BASE_URL = sys.argv[1]
    print(f"starting crawl of {BASE_URL}")

    page_data = crawl_page(BASE_URL)
    
    print(f"Total pages crawled: {len(page_data)}")
    for url, data in page_data.items():
        print(f"{url}: {data}")


if __name__ == "__main__":
    main()
