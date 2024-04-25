import os

import requests
from bs4 import BeautifulSoup
from typing import Union
import logging
import json
from .utils import Config, SciItem


PDF_PATH = './articles'
PROJECT_MAIL = os.getenv("PROJECT_MAIL")


class PdfParser:
    def __init__(self, doi: str, config: Config):
        self.doi = doi
        self.config = config
        self.path = None

    def parse(self) -> SciItem:
        self.path = rf'{PDF_PATH}/{self.doi.replace("&&&", "?").replace("https://", "&&").replace("http://", "&&").replace("/", "&") + ".pdf"}'
        item = self.parse_unpay()

        return item

    def parse_unpay(self) -> Union[SciItem, bool]:
        try:
            url = self._get_unpay_url()
            response = requests.get(url)
            download_url = self.prepare_unpay_download_url(response)
            self.download_article(download_url, self.path)

            return SciItem(
                file_url=download_url,
                DOI=self.doi,
                file_path=self.path
            )
        except Exception as e:
            logging.info(f"\n\nERROR EXCEPTION as {e}\n\n")
            return False

    @staticmethod
    def download_article(download_url: str, path: str):
        logging.info(f"\n\ndownload article start = {download_url}\n\n")
        try:
            logging.info(f"\n\ngetting response\n\n")
            r = requests.get(download_url, timeout=4)
            logging.info(f"\n\nurl = {download_url} and status_code = {r.status_code}\n\n")
        except Exception as e:
            logging.info(f"\n\nerror = {e}\n\n")
            raise AttributeError
        if r.status_code in (404, 403):
            raise AttributeError

        with open(path, 'wb') as f:
            f.write(r.content)

    def prepare_unpay_download_url(self, response):
        data = json.loads(response.text)
        url_location = data['best_oa_location']
        if not url_location or not url_location['url_for_pdf']:
            raise Exception('no pdf url')
        return url_location['url_for_pdf']

    def _get_unpay_url(self):
        doi = getattr(self, 'doi', None)
        return self.config.unpay_pdfs_url + "/" + doi + f"?email={PROJECT_MAIL}" if doi else None
