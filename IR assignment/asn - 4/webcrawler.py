import csv
import time
from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def crawl_website(start_url, max_pages=5):
    visited = set()
    queue = deque([start_url])

    start_domain = urlparse(start_url).netloc
    results = []

    headers = {
        "User-Agent": "StudentWebCrawler/1.0 (educational project)"
    }

    while queue and len(visited) < max_pages:
        url = queue.popleft()

        if url in visited:
            continue

        try:
            response = requests.get(
                url, headers=headers, timeout=10
            )
            response.raise_for_status()

            # Process HTML pages only
            content_type = response.headers.get(
                "Content-Type", ""
            )
            if "text/html" not in content_type.lower():
                continue

            visited.add(url)

            soup = BeautifulSoup(response.text, "html.parser")
            title = (
                soup.title.get_text(strip=True)
                if soup.title else "No title"
            )

            links = set()

            for tag in soup.find_all("a", href=True):
                link = urljoin(url, tag["href"])
                parsed = urlparse(link)

                # Keep only HTTP/HTTPS links on the same domain
                if (
                    parsed.scheme in ("http", "https")
                    and parsed.netloc == start_domain
                ):
                    clean_link = parsed._replace(
                        fragment=""
                    ).geturl()

                    links.add(clean_link)

            results.append({
                "url": url,
                "title": title,
                "links_found": len(links)
            })

            print("\nPage:", url)
            print("Title:", title)
            print("Links found:", len(links))

            for link in sorted(links):
                if link not in visited and link not in queue:
                    queue.append(link)

            # Avoid sending requests too quickly
            time.sleep(1)

        except requests.RequestException as error:
            print("Could not access", url, "-", error)

    # Save crawl results
    with open(
        "crawl_results.csv", "w",
        newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["url", "title", "links_found"]
        )
        writer.writeheader()
        writer.writerows(results)

    print("\nTotal pages visited:", len(visited))
    print("Results saved to crawl_results.csv")


if __name__ == "__main__":
    start = input("Enter the website URL: ").strip()

    if not start.startswith(("http://", "https://")):
        start = "https://" + start

    crawl_website(start, max_pages=5)