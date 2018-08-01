from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import config
import os
import plugin


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

if not os.path.exists('tmp'):
    os.makedirs('tmp')
fh = logging.FileHandler('./tmp/log.txt')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logging.getLogger('').addHandler(fh)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def check_authority(update):
    if update.message.chat.id == config.telegram_chatid:
        return True
    else:
        #update.message.reply_text('sorry, you are not my master.')
        return False

def start(bot, update):
    if not check_authority(update): return
    update.message.reply_text('Welcome my Master!')


def help(bot, update):
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')

def balance(bot, update):
    if not check_authority(update): return
    keyboard = [[InlineKeyboardButton("Bitmex", callback_data='bitmex.balance'),
                InlineKeyboardButton("Coinex", callback_data='coinex.balance')],
                [InlineKeyboardButton("Okex", callback_data='okex.balance'),
                InlineKeyboardButton("Bitstamp", callback_data='bitstamp.balance')],
                [InlineKeyboardButton("Combine", callback_data='combine.balance')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def ticker(bot, update):
    if not check_authority(update): return
    keyboard = [[InlineKeyboardButton("Bitmex", callback_data='bitmex.ticker'),
                InlineKeyboardButton("Coinex", callback_data='coinex.ticker')],
                [InlineKeyboardButton("Okex", callback_data='okex.ticker'),
                InlineKeyboardButton("Bitstamp", callback_data='bitstamp.ticker')],
                [InlineKeyboardButton("Combine", callback_data='combine.ticker')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def callback_query(bot, update):
    query = update.callback_query
    response = ''
    try:
        cmd = "plugin.%s()" % (query.data)
        response = eval(cmd)
    except Exception as e:
        response = 'exec %s failed!' % (query.data)
    

    bot.edit_message_text(text=response,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def alarm(bot, job):
    """Send the alarm message."""
    bot.send_message(job.context, text='Beep!')


def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    if not check_authority(update): return
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue
        job = job_queue.run_once(alarm, due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if not check_authority(update): return
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Timer successfully unset!')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def echo(bot, update):
    """Echo the user message."""
    if not check_authority(update): return
    update.message.reply_text(update.message.text)

def callback_func(bot, update):

    try:
        bot.delete_message(update.message.chat_id, update.message.message_id)
        logging.info('delete group join or left message: %d ' % update.message.message_id)
    except Exception as ex:
        if 'message to delete not found' in str(ex):
            logging.error('Failed to delete join message: %s' % ex)
        else:
            raise

def main():
    """Run bot."""
    updater = Updater(config.telegram_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("balance", balance))

    dp.add_handler(CommandHandler("ticker", ticker))

    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

    dp.add_handler(CallbackQueryHandler(callback_query))

    dp.add_handler(MessageHandler(Filters.text | Filters.command, echo))

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members | Filters.status_update.left_chat_member, callback_func))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        s=traceback.format_exc()
        logging.info(e)
        logging.error(s)