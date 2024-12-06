import os
import sys
from urllib.request import urlretrieve


def main():
    if len(sys.argv) != 2:
        exit("Usage: dl_wp_pdf ARTICLE_NAME")
    article = sys.argv[1]

    url = f"https://en.wikipedia.org/api/rest_v1/page/pdf/{article}"
    filename = f"{os.getcwd()}/{article}.pdf"

    path, headers = urlretrieve(url, filename)
    if headers.get("content-type") != "application/pdf":
        exit("The retrieved file is not a valid PDF.")
    else:
        print(f"--> {path}")


if __name__ == "__main__":
    main()
