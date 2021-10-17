import logging

import player
import messagesdualbot
import datetime
import collections

import configdualbot
import telegram
import dload ##important for parsing JSON htmls; to enable bot forwarding of images between bots
import requests

class Response(): ##Class for Telegram files
    def __init__(self):
        self.ok = None
        self.result = {}
        self.result["file_id"] = None
        self.result["file_unique_id"] = None
        self.result["file_size"] = None
        self.result["file_path"] = None


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, \
    CallbackQueryHandler

CHOOSING, ANGEL, MORTAL = range(3)

# Enable logging
logging.basicConfig(
    filename=f'logs/{datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")}.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

ANGEL_BOT_TOKEN = configdualbot.ANGEL_BOT_TOKEN
MORTAL_BOT_TOKEN = configdualbot.MORTAL_BOT_TOKEN

players = collections.defaultdict(player.Player)
player.loadPlayers(players)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start_Angelbot(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    playerName = update.message.chat.username.lower()


    if players[playerName].username is None:
        update.message.reply_text(messagesdualbot.NOT_REGISTERED)
        return

    players[playerName].chat_id = update.message.chat.id
    players[playerName].first_name = update.message.chat.first_name

    if players[playerName].chat_id is None:     ##just in case
        update.message.reply_text(messagesdualbot.ERROR_CHAT_ID)
        return

    logger.info(f'{playerName} started the bot with chat_id {players[playerName].chat_id}')

    send_menu_Angel = [
        [InlineKeyboardButton(f"Talk to my {configdualbot.ANGEL_ALIAS}", callback_data='angel')],
    ]
    reply_markup_Angel = InlineKeyboardMarkup(send_menu_Angel)
    update.message.reply_text(f'Hi {update.message.chat.first_name}! {messagesdualbot.HELP_TEXT_ANGEL}', reply_markup=reply_markup_Angel)

    return CHOOSING


def start_Mortalbot(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    playerName = update.message.chat.username.lower()
    if players[playerName].username is None:
        update.message.reply_text(messagesdualbot.NOT_REGISTERED)
        return

    players[playerName].chat_id = update.message.chat.id
    players[playerName].first_name = update.message.chat.first_name

    if players[playerName].chat_id is None: ##just in case
        update.message.reply_text(messagesdualbot.ERROR_CHAT_ID)
        return

    logger.info(f'{playerName} started the bot with chat_id {players[playerName].chat_id}')

    send_menu_Mortal = [
        [InlineKeyboardButton(f"Talk to my {configdualbot.MORTAL_ALIAS}", callback_data='mortal')],
    ]
    reply_markup_Mortal = InlineKeyboardMarkup(send_menu_Mortal)
    update.message.reply_text(f'Hi {update.message.chat.first_name}! {messagesdualbot.HELP_TEXT_MORTAL}', reply_markup=reply_markup_Mortal)

    return CHOOSING


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(messagesdualbot.HELP_TEXT_ANGEL)

def reload_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /savechatids is issued."""
    player.saveChatID(players)
    logger.info(f'Player chat ids have been saved in {configdualbot.CHAT_ID_JSON}')

    player.loadPlayers(players)
    logger.info(f'Players reloaded')

    update.message.reply_text(f'Players reloaded')

def mortal_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /mortal is issued."""
    playerName = update.message.chat.username.lower()
    update.message.reply_text(f"Your mortal is @{players[playerName].mortal.username}")


'''
Not used in dualbot
'''
# def send_command(update: Update, context: CallbackContext):
#     """Start send convo when the command /send is issued."""
#     playerName = update.message.chat.username.lower()
#
#     if players[playerName].username is None:
#         update.message.reply_text(messagesdualbot.NOT_REGISTERED)
#         return ConversationHandler.END
#
#     if players[playerName].chat_id is None:
#         update.message.reply_text(messagesdualbot.ERROR_CHAT_ID)
#         return ConversationHandler.END
#
#     send_menuAngel = [InlineKeyboardButton(configdualbot.ANGEL_ALIAS, callback_data='angel')]
#     send_menuMortal =[InlineKeyboardButton(configdualbot.MORTAL_ALIAS, callback_data='mortal')]
#     reply_markupAngel = InlineKeyboardMarkup(send_menuAngel)
#     reply_markupMortal = InlineKeyboardMarkup(send_menuMortal)
#     update.message.reply_text(messagesdualbot.SEND_COMMAND, reply_markup=reply_markup)
#
#     return CHOOSING


def startAngel(update: Update, context: CallbackContext):
    playerName = update.callback_query.message.chat.username.lower()
    if players[playerName].angel.chat_id is None:
        update.callback_query.message.reply_text(messagesdualbot.getBotNotStartedMessage(configdualbot.ANGEL_ALIAS))
        logger.info(messagesdualbot.getNotRegisteredLog(configdualbot.ANGEL_ALIAS, playerName, players[playerName].angel.username))
        return ConversationHandler.END ###test this function by removing choosing & putting ConversationHandler.END

    update.callback_query.message.reply_text(messagesdualbot.getPlayerMessage(configdualbot.ANGEL_ALIAS))
    return ANGEL


def startMortal(update: Update, context: CallbackContext):
    playerName = update.callback_query.message.chat.username.lower()
    if players[playerName].mortal.chat_id is None:
        update.callback_query.message.reply_text(messagesdualbot.getBotNotStartedMessage(configdualbot.MORTAL_ALIAS))
        logger.info(messagesdualbot.getNotRegisteredLog(configdualbot.MORTAL_ALIAS, playerName, players[playerName].mortal.username))
        return ConversationHandler.END ###test this function by removing choosing & putting ConversationHandler.END

    update.callback_query.message.reply_text(messagesdualbot.getPlayerMessage(configdualbot.MORTAL_ALIAS))
    return MORTAL

'''
message.photo example output:
[<telegram.files.photosize.PhotoSize object at 0x000001E862EC8880>, <telegram.files.photosize.PhotoSize object at 0x000001E862EC8AC0>, <telegram.files.photosize.PhotoSize object at 0x000001E862EC89A0>, <telegram.files.photosize.PhotoSize object at 0x000001E862EC8940>]
message.photo[-1] example output:
{'file_size': 126249, 'width': 720, 'file_unique_id': 'AQAD-7AxG9hWWFd-', 'file_id': 'AgACAgUAAxkBAAICG2FrmmQrkdsQZXXatT32MAG6_Z71AAL7sDEb2FZYVwZB8PbnNsibAQADAgADeQADIQQ', 'height': 1280}
'''

def sendNonTextMessageMortal(message, bot, chat_id):
    if message.photo:
        fileid = message.photo[-1]["file_id"]
        response = f"https://api.telegram.org/bot{MORTAL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{MORTAL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.content to get the bytes, then pass the bytes into the argument instead! :)
        logger.info(f"{filepath} // {htmllink}")
        bot.send_photo(
            photo=response2.content,
            caption=message.caption,
            chat_id=chat_id
        )
    elif message.sticker:
        bot.send_sticker(
            sticker=message.sticker,
            chat_id=chat_id
        )
    elif message.document:
        fileid = message.document["file_id"]
        response = f"https://api.telegram.org/bot{MORTAL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{MORTAL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.text to get the string, then pass the bytes into the argument instead! :)
        response2.encoding = 'utf-8' ##explicit encoding by setting .encoding before accessing .text
        bot.send_document(
            document=response2.content,
            filename=f"{filepath.split('/')[-1]}", ##sending in bytes loses the file name & file type. Not perfect, but this is probably the best solution.
            caption=message.caption,
            chat_id=chat_id
        )
    elif message.video:
        fileid = message.video["file_id"]
        response = f"https://api.telegram.org/bot{MORTAL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{MORTAL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.content to get the bytes, then pass the bytes into the argument instead! :)
        logger.info(f"{filepath} // {htmllink}")
        bot.send_video(
            video=response2.content,
            caption=message.caption,
            chat_id=chat_id
        )
    elif message.video_note:
        fileid = message.video_note["file_id"]
        response = f"https://api.telegram.org/bot{MORTAL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{MORTAL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.content to get the bytes, then pass the bytes into the argument instead! :)
        logger.info(f"{filepath} // {htmllink}")
        bot.send_video_note(
            video_note=response2.content,
            chat_id=chat_id
        )
    elif message.voice:
        fileid = message.voice["file_id"]
        response = f"https://api.telegram.org/bot{MORTAL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{MORTAL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.content to get the string, then pass the bytes into the argument instead! :)
        bot.send_voice(
            voice=response2.content,
            chat_id=chat_id
        )
    elif message.audio:
        fileid = message.audio["file_id"]
        response = f"https://api.telegram.org/bot{MORTAL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{MORTAL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.content to get the string, then pass the bytes into the argument instead! :)
        bot.send_audio(
            audio=response2.content,
            chat_id=chat_id
        )
    elif message.animation:
        fileid = message.animation["file_id"]
        response = f"https://api.telegram.org/bot{MORTAL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{MORTAL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.content to get the string, then pass the bytes into the argument instead! :)
        bot.send_animation(
            animation=response2.content,
            chat_id=chat_id
        )

def sendNonTextMessageAngel(message, bot, chat_id):
    if message.photo:
        fileid = message.photo[-1]["file_id"]
        response = f"https://api.telegram.org/bot{ANGEL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{ANGEL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.content to get the bytes, then pass the bytes into the argument instead! :)
        logger.info(f"{filepath} // {htmllink}")
        bot.send_photo(
            photo=response2.content,
            caption=message.caption,
            chat_id=chat_id
        )
    elif message.sticker:
        bot.send_sticker(
            sticker=message.sticker,
            chat_id=chat_id
        )
    elif message.document:
        fileid = message.document["file_id"]
        response = f"https://api.telegram.org/bot{ANGEL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{ANGEL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.text to get the string, then pass the bytes into the argument instead! :)
        response2.encoding = 'utf-8' ##explicit encoding by setting .encoding before accessing .text
        bot.send_document(
            document=response2.content,
            filename=f"{filepath.split('/')[-1]}", ##sending in bytes loses the file name & file type. Not perfect, but this is probably the best solution.
            caption=message.caption,
            chat_id=chat_id
        )
    elif message.video:
        fileid = message.video["file_id"]
        response = f"https://api.telegram.org/bot{ANGEL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{ANGEL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.content to get the bytes, then pass the bytes into the argument instead! :)
        logger.info(f"{filepath} // {htmllink}")
        bot.send_video(
            video=response2.content,
            caption=message.caption,
            chat_id=chat_id
        )
    elif message.video_note:
        fileid = message.video_note["file_id"]
        response = f"https://api.telegram.org/bot{ANGEL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{ANGEL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.content to get the bytes, then pass the bytes into the argument instead! :)
        logger.info(f"{filepath} // {htmllink}")
        bot.send_video_note(
            video_note=response2.content,
            chat_id=chat_id
        )
    elif message.voice:
        fileid = message.voice["file_id"]
        response = f"https://api.telegram.org/bot{ANGEL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{ANGEL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.content to get the string, then pass the bytes into the argument instead! :)
        bot.send_voice(
            voice=response2.content,
            chat_id=chat_id
        )
    elif message.audio:
        fileid = message.audio["file_id"]
        response = f"https://api.telegram.org/bot{ANGEL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{ANGEL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.content to get the string, then pass the bytes into the argument instead! :)
        bot.send_audio(
            audio=response2.content,
            chat_id=chat_id
        )
    elif message.animation:
        fileid = message.animation["file_id"]
        response = f"https://api.telegram.org/bot{ANGEL_BOT_TOKEN}/getFile?file_id={fileid}"
        logger.info(f"{fileid} // {response}")
        j = Response()
        j = dload.json(response)
        logger.info(dload.json(response))
        filepath = j["result"]["file_path"]
        htmllink = f"https://api.telegram.org/file/bot{ANGEL_BOT_TOKEN}/{filepath}"
        response2 = requests.get(htmllink)  ##Somehow, passing the html link into photo does NOT work.
        # Use response2.content to get the string, then pass the bytes into the argument instead! :)
        bot.send_animation(
            animation=response2.content,
            chat_id=chat_id
        )
    '''
    Fowarding polls probably doesn't work for now
    '''
    # elif message.poll:
    #     tempPoll = telegram.Poll(chat_id = None,
    #                             question = None,
    #                             options = None,
    #                             is_anonymous = None,
    #                             type = None,
    #                             allows_multiple_answers = None,
    #                             correct_option_id = None,
    #                             explanation = None,
    #                             open_period=None,
    #                             close_date= None,
    #                             id = None,
    #                             total_voter_count= None,
    #                             is_closed=None,
    #                  )
    #     tempPoll = message.poll
    #     tempOptions = []
    #     for x in message.poll.options:
    #         y = json.loads(x)
    #         tempOptions.append(y)
    #         logger.info (x, y)
    #     bot.send_poll(chat_id = chat_id,
    #                   question = tempPoll.question,
    #                   options = tempOptions,
    #                   is_anonymous = tempPoll.is_anonymous,
    #                   type = tempPoll.type,
    #                   allows_multiple_answers = tempPoll.allows_multiple_answers,
    #                   correct_option_id = tempPoll.correct_option_id,
    #                   explanation = tempPoll.explanation,
    #                   open_period=tempPoll.open_period,
    #                   close_date=tempPoll.close_date,
    #                   )








angelbotID = telegram.Bot(ANGEL_BOT_TOKEN)
mortalbotID = telegram.Bot(MORTAL_BOT_TOKEN)

def sendAngel(update: Update, context: CallbackContext, bot = mortalbotID):
    playerName = update.message.chat.username.lower()
    # logger.info(f'{context.bot}')
    if update.message.text:
        bot.send_message(
            text=update.message.text,
            chat_id=players[playerName].angel.chat_id
        )
    else:
        # context.bot.send_message(
        #     text=messages.getReceivedMessage(configdualbot.MORTAL_ALIAS),
        #     chat_id=players[playerName].angel.chat_id
        # )
        sendNonTextMessageAngel(update.message, bot, players[playerName].angel.chat_id)

    update.message.reply_text(messagesdualbot.MESSAGE_SENT)

    logger.info(messagesdualbot.getSentMessageLog(configdualbot.ANGEL_ALIAS, playerName, players[playerName].angel.username))

    return ANGEL


def sendMortal(update: Update, context: CallbackContext, bot = angelbotID):
    playerName = update.message.chat.username.lower()
    # logger.info(f'{context.bot}') ##to find out the current telegram.Bot Object being used
    if update.message.text:
        bot.send_message(
            text=update.message.text,
            chat_id=players[playerName].mortal.chat_id
        )
    else:
        # context.bot.send_message(
        #     text=messages.getReceivedMessage(configdualbot.MORTAL_ALIAS),
        #     chat_id=players[playerName].angel.chat_id
        # )
        sendNonTextMessageMortal(update.message, bot, players[playerName].mortal.chat_id)

    update.message.reply_text(messagesdualbot.MESSAGE_SENT)

    logger.info(messagesdualbot.getSentMessageLog(configdualbot.MORTAL_ALIAS, playerName, players[playerName].mortal.username))

    return MORTAL


def cancel(update: Update, context: CallbackContext) -> int:
    logger.info(f"{update.message.chat.username} canceled the conversation.")
    update.message.reply_text(
        'Sending message cancelled. Please type /start to chat again.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updaterMortal = Updater(MORTAL_BOT_TOKEN, use_context=True)
    # mortalbotID = botclass.Bot()
    # mortalbotID = updaterMortal.bot
    updaterAngel = Updater(ANGEL_BOT_TOKEN, use_context=True)
    # angelbotID = botclass.Bot()
    # angelbotID = updaterAngel.bot
    # botclass.saveBotID()
    # Get the dispatcher to register handlers
    dispatcherMortal = updaterMortal.dispatcher
    dispatcherAngel = updaterAngel.dispatcher
    # on different commands - answer in Telegram
    # dispatcherMortal.add_handler(CommandHandler("start", start_Mortal))
    dispatcherMortal.add_handler(CommandHandler("help", help_command))
    dispatcherMortal.add_handler(CommandHandler("savechatids", reload_command))
    dispatcherMortal.add_handler(CommandHandler("mortal", mortal_command))

    # dispatcherAngel.add_handler(CommandHandler("start", start_Angel))
    dispatcherAngel.add_handler(CommandHandler("help", help_command))
    dispatcherAngel.add_handler(CommandHandler("savechatids", reload_command))

    conv_handler_Angel = ConversationHandler(
        entry_points=[CommandHandler('start', start_Angelbot)],
        states={
            CHOOSING: [CallbackQueryHandler(startAngel, pattern='angel')],
            ANGEL: [MessageHandler(~Filters.command, sendAngel)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    conv_handler_Mortal = ConversationHandler(
        entry_points=[CommandHandler('start', start_Mortalbot)],
        states={
            CHOOSING: [CallbackQueryHandler(startMortal, pattern='mortal')],
            MORTAL: [MessageHandler(~Filters.command, sendMortal)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcherMortal.add_handler(conv_handler_Mortal)
    dispatcherAngel.add_handler(conv_handler_Angel)

    # Start the Bot
    updaterMortal.start_polling()
    updaterAngel.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updaterMortal.idle()
    updaterAngel.idle()


if __name__ == '__main__':
    try:
        main()
    finally:
        player.saveChatID(players)
        logger.info(f'Player chat ids have been saved in {configdualbot.CHAT_ID_JSON}')