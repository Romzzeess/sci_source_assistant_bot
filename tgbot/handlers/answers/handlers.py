import time

import joblib
import telegram
from telegram import Update
from telegram.ext import CallbackContext
from tgbot.handlers.utils.info import extract_user_data_from_update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .static_text import entry_assistant, confirm_start_assistant, send_pdf, texts
from tgbot.handlers.broadcast_message.utils import delete_message, send_one_message, send_document

from agents.summary import get_summary
from parser.get_articles import get_articles


PATH_FOUNDED = './resources/articles/founded'
PATH_RECEIVED = './resources/articles/received'
QUESTIONS_PATH = "./questions"


def answer_message(update: Update, context: CallbackContext):
    """ Type /broadcast <some_text>. Then check your message in HTML format and broadcast to users."""
    text = update.message.text
    user_id = extract_user_data_from_update(update)['user_id']

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

    articles, dois = get_articles(text)

    reply_markup = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(send_pdf, callback_data=text)
        ]]
    )

    delete_message(user_id=user_id, message_id=wait_massage.message_id)

    try:
        update.message.reply_text(
            text=f"{texts['summary_form']}{text}",
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=reply_markup
        )
    except telegram.error.BadRequest as e:
        if str(e) == "Button_data_invalid":
            update.message.reply_text(
                text=texts['long_text'],
                parse_mode=telegram.ParseMode.HTML,
            )

        else:
            update.message.reply_text(
                text=texts['error_with_html'].format(reason=e),
                parse_mode=telegram.ParseMode.HTML,
            )


def send_articles(update: Update, context: CallbackContext):
    query = update.callback_query.data

    articles = joblib.load(QUESTIONS_PATH + f"/{query}.joblib")
    user_id = extract_user_data_from_update(update)['user_id']

    for article in articles:
        send_one_message(user_id=user_id, text=str(article['meta']))
        send_document(user_id=user_id, file=article['path'])
