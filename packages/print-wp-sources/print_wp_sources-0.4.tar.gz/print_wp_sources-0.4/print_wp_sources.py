import sys
from urllib.parse import unquote
from urllib.request import urlopen

from bs4 import BeautifulSoup


def main():
    if len(sys.argv) != 2:
        exit("Usage: print-wp-sources ARTICLE_NAME")
    article = sys.argv[1]

    url = f"https://en.wikipedia.org/wiki/{article}"
    text = urlopen(url).read()
    soup = BeautifulSoup(text, "html.parser")
    for link in soup.find_all("a", attrs={"class": "external text"}):
        print(unquote(link.get("href")))


if __name__ == "__main__":
    main()
