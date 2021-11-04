#!/usr/bin/env python
# pylint: disable=C0116,W0613

import what3words
import logging
from telegram.ext import Updater, CommandHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
geocoder = what3words.Geocoder("your w3w token")
tgtoken = "your telegram bot token"

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def w3w(update, context):
    try:
        number1 = str(context.args[0])
        number2 = str(context.args[1])
        result = geocoder.convert_to_3wa(what3words.Coordinates(number1, number2))

        update.message.reply_text('The coordinates are: '+str(result))
    except (IndexError, ValueError):
        update.message.reply_text('There are not enough numbers')

def coords(update, context):
    try:
        word1 = str(context.args[0])
        word2 = str(context.args[1])
        word3 = str(context.args[2])

        result1 = geocoder.convert_to_coordinates(f"{word1}.{word2}.{word3}")

        update.message.reply_text('The 3 words are: '+str(result1))
    except (IndexError, ValueError):
        update.message.reply_text('There are not enough words')


def main():
    updater = Updater(tgtoken, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("w3w", w3w))
    dp.add_handler(CommandHandler("coords", coords))

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
