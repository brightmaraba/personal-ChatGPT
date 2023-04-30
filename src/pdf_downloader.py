#!/usr/bin/env python3
"""
Script to download pdfs from a website
"""

__author__ = "Brian Koech"
__version__ = "0.1.0"
__license__ = "MIT"

# import libraries
import os
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def name_formatter(pdf_file):
    """REGEX to format pdf file name removing unwanted characters
    :param pdf_file: pdf file name
    :return: formatted pdf file name
    """
    new_pdf_file_name = re.sub(r"%20-|%20|%2C|%28|%29", "_", pdf_file)
    new_pdf_file_name = re.sub(r"__", "_", new_pdf_file_name)
    new_pdf_file_name = re.sub(r"(-)\d{4}", r"\1", new_pdf_file_name)

    return new_pdf_file_name


def download_pdf_file(url):
    """Download files from url and save it locally.
    :param url: url to download files from
    :param count: number of files to be downloaded
    :return: True if file was downloaded, False otherwise
    """
    data_dir = "./data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # get the response from the url
    response = requests.get(url)
    # create a soup object
    soup = BeautifulSoup(response.content, "html.parser")
    # find all the links on the web page with the pdf extension
    for link in soup.select("a[href$='.pdf']"):
        # Name the pdf files using the last portion of each link which are unique in this case
        filename = os.path.join(data_dir, link["href"].split("/")[-1])
        filename = name_formatter(filename)
        with open(filename, "wb") as f:
            f.write(requests.get(urljoin(url, link["href"])).content)


if __name__ == "__main__":
    """This is executed when run from the command line"""
    download_pdf_file(
        "http://www.parliament.go.ke/the-national-assembly/house-business/hansard"
    )
