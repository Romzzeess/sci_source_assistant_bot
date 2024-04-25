from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io


def pdf_to_text(input_file):
	i_f = open(input_file, 'rb')
	resMgr = PDFResourceManager()
	retData = io.StringIO()
	TxtConverter = TextConverter(resMgr, retData, laparams=LAParams())
	interpreter = PDFPageInterpreter(resMgr, TxtConverter)
	for page in PDFPage.get_pages(i_f):
		interpreter.process_page(page)

	txt = retData.getvalue()

	if i := txt.find('REFERENCES') > len(txt) // 2:
		txt = txt[:i]

	if i := txt.find('REFERENCES') > len(txt) // 2:
		txt = txt[:i]

	if i := txt.find('REFERENCES') > len(txt) // 2:
		txt = txt[:i]

	return txt