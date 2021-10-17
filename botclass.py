'''
This py file is only important for dual bots
'''
import config
import csv
import json
import logging

logger = logging.getLogger(__name__)

class Bot():
    def __init__(self):
        self.id = 2048638397
        self.username = 'AngelsMortalsMNCbot'
        self.first_name = 'Your Angel Bot MedNurseClub'

def saveBotID():
    with open(config.BOT_ID_JSON, 'w+') as f:
        json.dump(angelbotID.__dict__, f)
        json.dump(mortalbotID.__dict__, f)


def loadBotID():
    try:
        with open(config.BOT_ID_JSON, 'r') as f:
            temp = json.load(f)
            logger.info(temp)
            output = Bot(**j) ##nvr got time to fix
    except:
        logger.warn('Fail to load bot ids')