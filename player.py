import config
import csv
import json
import logging

logger = logging.getLogger(__name__)


class Player():
    def __init__(self):
        self.username = None
        self.name = None
        self.angel = None
        self.mortal = None
        self.chat_id = None


def loadPlayers(players: dict):
    with open(config.PLAYERS_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                logger.info(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                playerName = row[0].strip().lower()
                angelName = row[1].strip().lower()
                mortalName = row[2].strip().lower()
                logger.info(f'\t{playerName} has angel {angelName} and mortal {mortalName}.')
                players[playerName].username = playerName
                players[playerName].angel = players[angelName]
                players[playerName].mortal = players[mortalName]
                line_count += 1
        logger.info(f'Processed {line_count} lines.')
    savemortalUsername(players)
    validatePairings(players)
    loadChatID(players)


def validatePairings(players: dict):
    for _, player in players.items():
        if player.angel.mortal.username != player.username or player.mortal.angel.username != player.username:
            print(f'Error with {player.username} pairings')
            logger.error(f'Error with {player.username} pairings')
            exit(1)

    logger.info(f'Validation complete, no issues with pairings.')


def savemortalUsername(players: dict): ##Important for mortal_command
    temp = {}
    for k, v in players.items():
        temp[k] = v.mortal.username

    with open(config.MORTAL_USERNAME_JSON, 'w+') as f:
        json.dump(temp, f)

def saveChatID(players: dict):
    temp = {}
    temp2 = {}
    for k, v in players.items():
        temp[k] = v.chat_id
        temp2[k] = v.first_name

    with open(config.CHAT_ID_JSON, 'w+') as f:
        json.dump(temp, f)

    with open(config.FIRST_NAME_JSON, 'w+') as f: ##saves first_names too
        json.dump(temp2, f)

def loadChatID(players: dict):
    try:
        with open(config.CHAT_ID_JSON, 'r') as f:
            temp = json.load(f)
            logger.info(temp)
            for k, v in temp.items():
                players[k].chat_id = v

        with open(config.NAME_JSON, 'r') as f: ##loads first_names too
            temp = json.load(f)
            logger.info(temp)
            for k, v in temp.items():
                players[k].name = v

        with open(config.MORTAL_USERNAME_JSON, 'r') as f:
            temp = json.load(f)
            logger.info(temp)
            for k, v in temp.items():
                players[k].mortal.username = v

    except:
        logger.warn('Fail to load chat ids')