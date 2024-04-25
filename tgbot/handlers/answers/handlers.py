import os

import joblib
import telegram
from telegram import Update
from telegram.ext import CallbackContext
from tgbot.handlers.utils.info import extract_user_data_from_update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .static_text import send_pdf, texts
from tgbot.handlers.broadcast_message.utils import delete_message, send_one_message, send_document

from agents.summary import summarize_documents, translate_to_en
from parser.get_articles import get_articles


PATH_FOUNDED = './resources/articles/founded'
PATH_RECEIVED = './resources/articles/received'
QUESTIONS_PATH = "./questions"
PDF_PATH = "./articles"


def answer_message(update: Update, context: CallbackContext):
    text = update.message.text

    if len(text) > 64:
        update.message.reply_text(
            text=texts['long_text'],
            parse_mode=telegram.ParseMode.HTML,
        )
        return

    try:
        wait_massage = update.message.reply_text(
            text=texts['waiting_message'],
            parse_mode=telegram.ParseMode.HTML,
        )
    except telegram.error.BadRequest as e:
        update.message.reply_text(
            text=texts['error_with_html'].format(reason=e),
            parse_mode=telegram.ParseMode.HTML,
        )

    en_text = translate_to_en(text)

    user_id = extract_user_data_from_update(update)['user_id']

    if not os.path.exists(QUESTIONS_PATH + f"/{text}.joblib"):
        articles, dois = get_articles(answer=en_text)

    else:
        articles = joblib.load(QUESTIONS_PATH + f"/{text}.joblib")

    if len(articles) == 0:
        update.message.reply_text(
            text=texts['unfound'],
            parse_mode=telegram.ParseMode.HTML,
        )
        return

    summary = summarize_documents([article['text'] for article in articles])

    reply_markup = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(send_pdf, callback_data=text),
            # InlineKeyboardButton(entry_assistant, callback_data=text)
        ]]
    )

    delete_message(user_id=user_id, message_id=wait_massage.message_id)

    try:
        update.message.reply_text(
            text=f"{texts['summary_form']}{summary}",
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=reply_markup
        )
    except telegram.error.BadRequest as e:
        update.message.reply_text(
            text=texts['error_with_html'].format(reason=e),
            parse_mode=telegram.ParseMode.HTML,
        )


def send_articles(update: Update, context: CallbackContext):
    query = update.callback_query.data

    articles = joblib.load(QUESTIONS_PATH + f"/{query}.joblib")
    user_id = extract_user_data_from_update(update)['user_id']

    for i in range(len(articles)):
        meta = articles[i]['meta']
        authors = meta.author.strip() if meta.author else 'Unknown'
        title = meta.title.strip()
        date = meta.date.strip().split(",")[0]
        page = meta.page.strip()
        source = f'<a href="https://doi.org/{meta.DOI.strip()}">{meta.DOI.strip()}</a>'
        meta_text = f'<code>{i + 1}. {authors.strip()}. {title}.{date} {page}.</code>\n\n' \
                    f'🔗 {source}\n' \

        send_one_message(user_id=user_id, text=meta_text)
        send_document(user_id=user_id, file=articles[i]['path'])
