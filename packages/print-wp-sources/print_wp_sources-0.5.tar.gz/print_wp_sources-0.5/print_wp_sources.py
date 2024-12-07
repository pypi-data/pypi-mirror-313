import sys

import requests
from bs4 import BeautifulSoup


def main():
    if len(sys.argv) != 2:
        exit("Usage: print-wp-sources ARTICLE_URL")
    article_url = sys.argv[1]

    text = requests.get(article_url).text
    soup = BeautifulSoup(text, "html.parser")
    for link in soup.find_all("a", attrs={"class": "external text"}):
        if "wikimediafoundation.org" not in link.get(
            "href"
        ) and "foundation.wikimedia.org" not in link.get("href"):
            print(link.get("href"))


if __name__ == "__main__":
    main()
