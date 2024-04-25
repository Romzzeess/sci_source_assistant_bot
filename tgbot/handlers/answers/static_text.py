from typing import Dict


texts: Dict[str, str] = {
	'enter': 'Введите свой запрос:',
	'error_with_html': "Не удается проанализировать ваш текст в стиле <code>HTML</code>. Причина: \n{reason}",
	'waiting_message': "Формируем отчет...",
	'summary_form': "Вот что удалось найти:\n\n",
	'long_text': "max length texts is 64 symbols"

}

entry_assistant = "ИИ ассистент"
confirm_start_assistant = "Введите ваш вопрос"
send_pdf = "PDF"