# Need to create a telegram bot, then interface with it here using the python-telegram-bot library

import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
import SemiFluentBot
import os

token = os.environ['TELEGRAM_TOKEN']
loading_gif = "https://d13yacurqjgara.cloudfront.net/users/552485/screenshots/1769328/progress.gif"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

CHOICES, WHERE = range(2)


def start(bot, update):
    reply_keyboard = [['ShowerThoughts', 'LifeProTips', 'UnethicalLifeProTips']]

    logger.info("Received start command.")
    update.message.reply_text('Hi! Send /cancel to stop talking to me.')
    update.message.reply_text('Which subreddit should I look at?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return WHERE


def where(bot, update):
    logger.info("Received subreddit choice. Fetching posts.")
    update.message.reply_text('Let me fetch some posts. Hang on.')
    update.message.reply_text(loading_gif)
    translated_options = SemiFluentBot.produce_output(update.message.text)

    update.message.reply_text(
        'Hello! Here are your options:\n\n')
    for option in translated_options:
        update.message.reply_text(option)
    update.message.reply_text('Send /cancel to stop talking to me.\n\n'
                              'What are your choices?')

    logger.info("Sent all the posts successfully, waiting for input.")

    return CHOICES


def choices(bot, update):
    user = update.message.from_user
    logger.info("Choices of %s: %s", user.first_name, update.message.text)
    logger.info('Sending to SFB.receive_input. Will be posted to reddit.')
    update.message.reply_text('You just said "' + update.message.text + '". \n Posting to Reddit now, give me a second.\n')
    SemiFluentBot.receive_input(update.message.text)
    update.message.reply_text('Posted! (Probably)')
    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def error(bot, update, error):
    # Just runs main() again when an error is caught.
    update.message.reply_text('Oh! Hit an error. Let me try to restart.')  # Added for timeout handling (?)
    main()  # Added for timeout handling (?)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(os.environ['STARTUP_KEY'], start)],  # no longer using '/start' as entry point, restricts access to bot. Put whatever string you want in auth.py

        states={
            WHERE: [MessageHandler(Filters.text, where)],
            CHOICES: [MessageHandler(Filters.text, choices)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    logger.info("Start_Polling")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
