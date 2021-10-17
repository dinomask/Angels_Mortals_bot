import config

MESSAGE_SENT = 'Message sent!'
HELP_TEXT_ANGEL = (
    f'Please click the button below to start messaging your {config.ANGEL_ALIAS}!'
    f'\n\n'
    f'This bot supports forwarding text, photos, stickers, documents, audio, video, and animations but not emojis.'
)
HELP_TEXT_MORTAL = (
    f'Please click the button below to start messaging your {config.MORTAL_ALIAS}!'
    f'\n\n'
    f'This bot supports forwarding text, photos, stickers, documents, audio, video, and animations but not emojis.'
    f'\n\n'
    f'Type /mortal to see who your mortal is!'
    f'\n\n'
    f"Type /start if your messages aren't getting sent"
)
ERROR_CHAT_ID = 'Sorry an error occurred please type /start again'
SEND_COMMAND = 'Send a message to my:\n'
NOT_REGISTERED = 'Sorry you are not registered with the game currently'

def getBotNotStartedMessage(alias):
    return f'Sorry your {alias} has not started this bot'

def getPlayerMessage(alias):
    return f'From now on all your messages will be sent to you {alias}\nHave fun typing!'

'''
not used in dualbot
'''
# def getReceivedMessage(alias, text=""):
#     return f"Message from your {alias}:\n\n{text}" if text != "" else f"Message from your {alias}:"

def getSentMessageLog(alias, sender, receiver):
    return f'{sender} sent a message to their {alias} {receiver}'

def getNotRegisteredLog(alias, sender, receiver):
    return f'{sender} {alias} {receiver} has not started the bot'