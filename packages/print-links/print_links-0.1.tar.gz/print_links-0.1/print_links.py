#!/usr/bin/env python3

import re
import sys

import requests
from bs4 import BeautifulSoup


def main():
    if len(sys.argv) != 2:
        exit("Usage: print-links URL")
    url = sys.argv[1]

    text = requests.get(url).text
    soup = BeautifulSoup(text, "html.parser")

    links = set()
    for link in soup.find_all("a"):
        links.add(link.get("href"))

    for link in links:
        if link.endswith("/") or link.endswith(".html"):
            match_str = re.search(r"\d{4}\/\d{2}\/\d{2}\/\w", link)
            if match_str:
                print(link)


if __name__ == "__main__":
    main()
