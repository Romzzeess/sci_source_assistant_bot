import os

import joblib
import requests

import logging

from .pdf_article import PdfParser
from .crossref import CrossrefParser
from .pdf_to_text import pdf_to_text
from .utils import Config


QUESTIONS_PATH = "./questions"
PDF_PATH = './articles'




def get_articles(answer: str, count=3, max_try=25, config=Config()):
	articles = []
	dois = []
	i = 0

	while (len(dois) < max_try - count) & (len(articles) < count):

		url = config.crossref_url + f'?query={answer}&offset={i}&rows=1'

		try:
			response = requests.get(url)
			data = response.json()['message']
		except Exception as e:
			logging.info(f"Error in parsing Crossref e = {e}")
			pass

		doi = data["items"][0]["DOI"]

		try:
			pdf = PdfParser(doi=doi, config=config).parse()
		except Exception as e:
			logging.info(f"Error in parsing PDF e = {e}")
			pass

		if pdf:
			try:
				articles.append({
					"meta": CrossrefParser(doi, config).parse(),
					"text": pdf_to_text(pdf.file_path),
					"path": pdf.file_path
				})
			except Exception as e:
				logging.info(f"Error in read PDF e = {e}")
				pass
		else:
			dois.append(doi)

		i += 1

	if not os.path.isdir("QUESTIONS_PATH"):
		os.mkdir("QUESTIONS_PATH")

	joblib.dump(articles, QUESTIONS_PATH + f"/{answer}.joblib")

	return articles, dois
