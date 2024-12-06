# dl-wp-pdf

This program just downloads a Wikipedia article as a PDF by using the Wikipedia REST API.

## Installation

``` shell
pipx install dl-wp-pdf
```

## Usage

Use the Wikipedia article's name as the argument to `dl-wp-pdf`. For example, if the article's URL is `https://en.wikipedia.org/wiki/Python_(programming_language)`, then the argument for `dl-wp-pdf` would be `"Python_(programming_language)"`.

``` shell
cd ~/downloads
dl-wp-pdf "Python_(programming_language)"

Output:
--> /home/jas/downloads/Python_(programming_language).pdf
```

> Note: make sure to use quotes around the article name in the argument to `dl-wp-pdf`.
