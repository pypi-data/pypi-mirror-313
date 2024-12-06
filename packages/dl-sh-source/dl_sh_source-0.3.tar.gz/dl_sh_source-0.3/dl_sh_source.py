import os
import sys

import requests
from bs4 import BeautifulSoup


def main():
    if len(sys.argv) != 3:
        exit("Usage: dl-sh-source SCIHUB_URL ARTICLE_URL")
    scihub = sys.argv[1]
    article = sys.argv[2]

    url = f"{scihub}/{article}"
    text = requests.get(url).text
    soup = BeautifulSoup(text, "html.parser")
    if str(soup.find("p")) == '<p id="smile">:(</p>':
        print(":(")
        exit(f"Unfortunately, Sci-Hub doesn't have the requested document: {article}")
    elif soup.find("button"):
        pdf_url = soup.find("button")["onclick"].split("//")[1].split("?")[0]
        article_url = f"https://{pdf_url}"
        filename = f"{os.getcwd()}/{os.path.basename(pdf_url)}"
        with requests.get(article_url, stream=True) as r:
            r.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"--> {filename}")
    else:
        exit("An as-yet unknown error occurred. Sorry for the inconvenience.")


if __name__ == "__main__":
    main()
