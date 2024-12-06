# dl-sh-source

This program downloads an article from Sci-Hub to the current working directory.

## Installation

``` shell
pipx install dl-sh-source --include-deps
```

## Usage

Use the original article's digital object identifier (DOI) for the ARTICLE_NAME argument. Use a working Sci-Hub proxy as the SCIHUB_URL argument. For example, if the article's DOI URL is `10.1192/bjp.173.6.519`, and the Sci-Hub proxy you want to use is `https://sci-hub.st`, then the entire command would look like the following:

``` shell
cd ~/downloads
dl-sh-source "https://sci-hub.st" "10.1192/bjp.173.6.519"

Output:
--> /home/jas/downloads/paykel1998.pdf
```

However, if the article cannot be found on Sci-Hub, you'll get the following message:

``` shell
Output:
:(
Unfortunately, Sci-Hub doesn't have the requested document: 10.1192/bjp.173.6.519
```

> Note: make sure to use quotes around the Sci-Hub URL and DOI in the arguments to `dl-sh-source`.
