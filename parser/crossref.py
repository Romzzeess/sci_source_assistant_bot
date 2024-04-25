import requests
from requests import Response

from bs4 import BeautifulSoup

from typing import Union

import logging

from .utils import Config, CrossRefItem


def filter_field(text: str) -> str:
    return BeautifulSoup(text, "lxml").text.replace("<", "").replace(">", "")


class CrossrefParser:
    def __init__(self, doi: str, config: Config):
        self.doi = doi
        self.config = config

    def parse(self) -> Union[CrossRefItem, bool]:
        url = self._get_url()
        try:
            response = requests.get(url)
            return self._serialize(response)
        except Exception as e:
            logging.info(f"Error in parsing Crossref e = {e}")
            return False

    def _get_url(self) -> str:
        doi = getattr(self, 'doi', None)
        return self.config.crossref_url + "/" + doi if doi else None

    def _serialize(self, response: Response) -> CrossRefItem:
        data = response.json()['message']
        item = CrossRefItem(
            title=data.get('title', ''),
            type=data.get('type', ''),
            author=data.get('author', ''),
            container_title=data.get('container-title', ''),
            date=data['created']['date-parts'],
            DOI=data['DOI'],
            ISSN=data.get('ISSN', ''),
            page=data.get('page', ''),
            volume=data.get('volume', ''),
            issue=data.get('issue', ''),
            is_installed=self.config.is_installed
        )
        return self._clean_item(item)

    @staticmethod
    def _clean_item(item: CrossRefItem):
        if item.ISSN:
            item.ISSN = ", ".join(item.ISSN)
        if item.container_title:
            item.container_title = ", ".join(item.container_title)
        if item.author:
            item.author = ", ".join([f"{x['given']} {x['family']}" if 'given' in x else "" for x in item.author])
        if item.date:
            item.date = str(item.date[0][0])
        if item.title:
            title = ", ".join(item.title)
            item.title = title if ">" not in title else filter_field(title)
        if item.DOI:
            doi = item.DOI
            item.DOI = doi if ">" not in doi else filter_field(doi)
        return item
