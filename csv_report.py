import csv 
from crawl import crawl_page

def write_csv_report(page_data, filename="report.csv"):
    with open("report.csv", "w", newline="", encoding="utf-8") as file:
        fieldNames = ["page_url", "h1", "first_paragraph", "outgoing_link_urls", "image_urls"]
        writer = csv.DictWriter(file, fieldNames=fieldNames)

        writer.writeheader()
        for each page in page_data.values():
            writer.writerow(page_data)
            ";".join(page["outgoing_links"])

