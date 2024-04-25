from typing import Dict


texts: Dict[str, str] = {
	'enter': 'Введите интересующий вас вопрос:',
	'error_with_html': "Не удается проанализировать ваш текст в стиле <code>HTML</code>. Причина: \n{reason}",
	'waiting_message': "Усердно думаем...",
	'summary_form': "Описание от ИИ-ассистента:\n\n",
	'long_text': "Максимальная длина вопроса - 64 символа, пожалуйста перефразируйте",
	'unfound': "Мы не смогли найти статьи по данной теме"

}

entry_assistant = "ИИ ассистент"
confirm_start_assistant = "Введите ваш вопрос"
send_pdf = "Показать использованные статьи"