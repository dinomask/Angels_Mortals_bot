import copy

import configdualbot
from telegram import messageentity

MESSAGE_SENT = 'Message sent!'
MESSAGE_SENT_TO_GAMEMASTER = 'Message sent to the Game Master! You may now click other buttons in the main menu.'
HELP_TEXT_ANGEL = (
    f'This bot supports forwarding text, emojis, photos, stickers, documents, audio, videos, and animations.'
    f'\n\n'
    f"Type /start if your messages aren't getting sent"
    f'\n\n'
    f'Please click the buttons below to find out more about your {configdualbot.ANGEL_ALIAS}\n\n'
    f'After that, you may click the button below to start messaging your {configdualbot.ANGEL_ALIAS} anonymously!'
)
HELP_TEXT_MORTAL = (
    f'This bot supports forwarding text, emojis, photos, stickers, documents, audio, videos, and animations.'
    f'\n\n'
    f"Type /start if your messages aren't getting sent"
    f'\n\n'
    f'Please click the buttons below to find out more about your {configdualbot.MORTAL_ALIAS}\n\n'
    f'After that, you may click the button below to start messaging your {configdualbot.MORTAL_ALIAS} anonymously!'
)
ERROR_CHAT_ID = f'Sorry an error occurred please type /start again'
# SEND_COMMAND = f'Send a message to my:\n'
NOT_REGISTERED = f'Sorry you are not registered with the game currently'
def STOPPED_BOT(alias):
    return f'Sorry, your message could not be sent. Either you have made an illegal message, or your {alias} has stopped the bot. They must restart it for your messages to be sent.\n\nPlease type your message again.'

def getBotNotStartedMessage(alias):
    return f'Sorry your {alias} has not started this bot yet.\n' \
           f'Please try again later.'

def getPlayerMessage(alias):
    return f'From now on, all your messages will be sent to your {alias}. Have fun chatting!\n\n' \
           f'Type /cancel if you want to go back and find out more about your {alias}\n\n'
           # f"Type /start again if your messages somehow aren't getting sent"

def getSupportMessage():
    return f"Facing an issue? Got a suggestion?\n\n"\
           f'Please type a description of your problem or feedback to be sent to the Game Master.\n\n' \
           f"Type /cancel to go back to the main menu."


'''
not used in dualbot
'''
# def getReceivedMessage(alias, text=""):
#     return f"Message from your {alias}:\n\n{text}" if text != "" else f"Message from your {alias}:"

def getSentMessageLog(alias, sender, receiver):
    return f'{sender} sent a message to their {alias} {receiver}'

def getNotRegisteredLog(alias, sender, receiver):
    return f'{sender} {alias} {receiver} has not started the bot'

def getMessageEntitybyYou(UpdateMessageText, UpdateReplyToMessageText, UpdateMessageEntities):
    effective_message_max_offset_length = len(UpdateMessageText)
    # print(effective_message_max_offset_length)
    max_length_reply_message = len(UpdateReplyToMessageText)
    # print(max_length_reply_message)
    offset_length_before_reply_message = effective_message_max_offset_length + 28  ##28 is the number of char in bot.send_message with reply, "You" template
    # print(offset_length_before_reply_message)
    list_of_entities = copy.deepcopy(UpdateMessageEntities)
    bold_entity01 = messageentity.MessageEntity(type="bold", offset=offset_length_before_reply_message - 26,
                                                         length=1)
    bold_entity02 = messageentity.MessageEntity(type="bold", offset=offset_length_before_reply_message - 10,
                                                         length=6)
    bold_entity03 = messageentity.MessageEntity(type="bold", offset=offset_length_before_reply_message - 3,
                                                         length=1)
    italic_entity01 = messageentity.MessageEntity(type="italic", offset=offset_length_before_reply_message,
                                                           length=max_length_reply_message)
    underline_entity = messageentity.MessageEntity(type="underline",
                                                            offset=offset_length_before_reply_message - 23, length=12)
    list_of_entities.append(bold_entity01)
    list_of_entities.append(bold_entity02)
    list_of_entities.append(bold_entity03)
    list_of_entities.append(italic_entity01)
    list_of_entities.append(underline_entity)
    return list_of_entities

def getMessageEntitybyYourALIAS(UpdateMessageText, UpdateReplyToMessageText, UpdateMessageEntities, LenALIAS):
    effective_message_max_offset_length = len(UpdateMessageText)
    # print(effective_message_max_offset_length)
    max_length_reply_message = len(UpdateReplyToMessageText)
    # print(max_length_reply_message)
    offset_length_before_reply_message = effective_message_max_offset_length + 30 + LenALIAS  ##30 + LenALIAS is the number of char in bot.send_message with reply, "You" template
    # print(offset_length_before_reply_message)
    list_of_entities = copy.deepcopy(UpdateMessageEntities)
    bold_entity01 = messageentity.MessageEntity(type="bold", offset=offset_length_before_reply_message - 28 - LenALIAS,
                                                         length=1)
    bold_entity02 = messageentity.MessageEntity(type="bold", offset=offset_length_before_reply_message - 12 - LenALIAS,
                                                         length=8 + LenALIAS)
    bold_entity03 = messageentity.MessageEntity(type="bold", offset=offset_length_before_reply_message - 3,
                                                         length=1)
    italic_entity01 = messageentity.MessageEntity(type="italic", offset=offset_length_before_reply_message,
                                                           length=max_length_reply_message)
    underline_entity = messageentity.MessageEntity(type="underline",
                                                            offset=offset_length_before_reply_message - 25 - LenALIAS, length=12)
    list_of_entities.append(bold_entity01)
    list_of_entities.append(bold_entity02)
    list_of_entities.append(bold_entity03)
    list_of_entities.append(italic_entity01)
    list_of_entities.append(underline_entity)
    return list_of_entities


def getMessageEntitybyYou_NoText(UpdateReplyToMessageText, UpdateMessageEntities):
    max_length_reply_message = len(UpdateReplyToMessageText)
    # print(max_length_reply_message)
    offset_length_before_reply_message = 26  ##26 is the number of char in bot.send_message with reply, "You" template
    # print(offset_length_before_reply_message)
    list_of_entities = copy.deepcopy(UpdateMessageEntities)
    bold_entity01 = messageentity.MessageEntity(type="bold", offset=offset_length_before_reply_message - 26,
                                                         length=1)
    bold_entity02 = messageentity.MessageEntity(type="bold", offset=offset_length_before_reply_message - 10,
                                                         length=6)
    bold_entity03 = messageentity.MessageEntity(type="bold", offset=offset_length_before_reply_message - 3,
                                                         length=1)
    italic_entity01 = messageentity.MessageEntity(type="italic", offset=offset_length_before_reply_message,
                                                           length=max_length_reply_message)
    underline_entity = messageentity.MessageEntity(type="underline",
                                                            offset=offset_length_before_reply_message - 23, length=12)
    list_of_entities.append(bold_entity01)
    list_of_entities.append(bold_entity02)
    list_of_entities.append(bold_entity03)
    list_of_entities.append(italic_entity01)
    list_of_entities.append(underline_entity)
    return list_of_entities

def getMessageEntitybyYourALIAS_NoText(UpdateReplyToMessageText, UpdateMessageEntities, LenALIAS):
    max_length_reply_message = len(UpdateReplyToMessageText)
    # print(max_length_reply_message)
    offset_length_before_reply_message = 28 + LenALIAS  ##28 + LenALIAS is the number of char in bot.send_message with reply, "You" template
    # print(offset_length_before_reply_message)
    list_of_entities = copy.deepcopy(UpdateMessageEntities)
    bold_entity01 = messageentity.MessageEntity(type="bold", offset=offset_length_before_reply_message - 28 - LenALIAS,
                                                         length=1)
    bold_entity02 = messageentity.MessageEntity(type="bold", offset=offset_length_before_reply_message - 12 - LenALIAS,
                                                         length=8 + LenALIAS)
    bold_entity03 = messageentity.MessageEntity(type="bold", offset=offset_length_before_reply_message - 3,
                                                         length=1)
    italic_entity01 = messageentity.MessageEntity(type="italic", offset=offset_length_before_reply_message,
                                                           length=max_length_reply_message)
    underline_entity = messageentity.MessageEntity(type="underline",
                                                            offset=offset_length_before_reply_message - 25 - LenALIAS, length=12)
    list_of_entities.append(bold_entity01)
    list_of_entities.append(bold_entity02)
    list_of_entities.append(bold_entity03)
    list_of_entities.append(italic_entity01)
    list_of_entities.append(underline_entity)
    return list_of_entities
