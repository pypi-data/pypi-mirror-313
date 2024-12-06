from __future__ import annotations
import re
from typing import Optional
import logging
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from func_timeout import func_timeout, FunctionTimedOut
from selenium.webdriver.chrome.options import Options
from holytools.web.link_soup import LinkSoup
# ---------------------------------------------------------


class SiteVisitor:
    max_site_loading_time = 10

    def __init__(self, headless : bool = True):
        chrome_options = Options()
        chrome_options.add_argument("--enable-javascript")
        if headless:
            chrome_options.add_argument("--headless")
        prefs = {
            "download.default_directory": "/dev/null",
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.last_url : Optional[str] = None


    def get_mail_addresses(self, url : str) -> list[str]:
        return get_mail_addresses_in_text(text=self.get_html(url=url))


    def get_text(self, url: str, with_links : bool = False) -> str:
        def do_extract_text() -> str:
            return self._extract_text(page_html=page_html, with_links=with_links)
        page_html = self.get_html(url=url)
        site_text = func_timeout(timeout=SiteVisitor.max_site_loading_time, func=do_extract_text)
        return site_text


    def get_html(self, url: str) -> str:
        try:
            result = self._fetch_site_html(url)
        except FunctionTimedOut:
            logging.warning(f'Failed to retrieve text from website {url} due to '
                            f'timeout after {SiteVisitor.max_site_loading_time} seconds')
            result = ''

        return result

    @staticmethod
    def _extract_text(page_html : str, with_links : bool = False) -> str:
        SoupType = LinkSoup if with_links else BeautifulSoup
        soup = SoupType(page_html, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        site_text = soup.get_text()
        lines = (line.strip() for line in site_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return '\n'.join(chunk for chunk in chunks if chunk)


    def _fetch_site_html(self, url: str) -> str:
        def get_website_html():
            if self.last_url != url:
                self.driver.get(url)
            return self.driver.page_source

        content = func_timeout(timeout=SiteVisitor.max_site_loading_time, func=get_website_html)
        self.last_url = url
        return content


    @staticmethod
    def site_exists(url : str, verbose : bool = False) -> bool:
        try:
            requests.get(url, timeout=10)
            return True
        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"Error: {e}")
        return False


    def __del__(self):
        self.quit()

    def quit(self):
        self.driver.quit()



def get_mail_addresses_in_text(text: str) -> list[str]:
    username_part = r'[A-Za-z0-9._%+-]+'
    domain_part = r'[A-Za-z0-9.-]+'
    tld_part = r'[A-Z|a-z]{2,}'
    at_symbol = r'(?:@|\[at\]| \[at\] )'  # Non-capturing group

    email_pattern = fr'\b{username_part}{at_symbol}{domain_part}\.{tld_part}\b'

    mail_addresses = re.findall(email_pattern, text)
    mail_addresses = [address.replace(' [at] ', '@') for address in mail_addresses]
    mail_addresses = [address.replace('[at]', '@') for address in mail_addresses]

    return mail_addresses
