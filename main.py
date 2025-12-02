import sys
import asyncio
from crawl import crawl_site_async


async def main():
    args = sys.argv
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    if len(args) > 4:
        print("too many arguments provided")
        sys.exit(1)

    base_url = args[1]
    max_concurrency = int(args[2])
    max_pages = int(args[3])

    print(f"Starting async crawl of: {base_url}")

    page_data = await crawl_site_async(base_url, max_concurrency, max_pages)

    for page in page_data.values():
        print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")

    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
