import variables as var
from bs4 import BeautifulSoup as bSoup
from urllib.request import urlopen as ureq
from urllib.error import HTTPError as error


def prepare_url(url):
    retry_count = 0
    try:
        u_client = ureq(url)
        page_html = u_client.read()
        u_client.close()
        return bSoup(page_html, "html.parser")
    except error:
        retry_count += 1
        if retry_count > 3:
            print("Exceeded retry count, skipping url")
            return None
        else:
            print("Error in preparing url, trying again")
            prepare_url(url)