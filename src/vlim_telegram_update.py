import telegram
import logging

from telegram.error import NetworkError

import bot

logger = bot.get_logger("VLIM Bot")
# logger.setLevel(logging.INFO)
# logger.addHandler(logging.StreamHandler())

def getUpdates():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    bot = telegram.Bot(token='322557664:AAGFsLMC9Fp78oFfB28sF99v-ZHLHfyUdIc')

    contacts = []
    contact = {}
    contacts.append(contact.update({
        'name'  : 'Tino',
        'id'    : '293534239'
    }))

    # print bot.getMe()
    # store_updates = []

    updates = []

    try:
        updates = bot.getUpdates()
    except NetworkError:
        logger.error("except NetworkError")
        bot.run()

    # print len(updates)
    # print([u.message.text for u in updates])
    # print([str(update.message.chat_id) + " : " + str(update.message.text) for update in updates])

    # for update in updates:
    #     ms = update.message
    #     if ms.chat.first_name:
    #         # print "[%s : %s] : %s" % (ms.date, ms.chat.first_name, ms.text)
    #         print "[%s : %s : %s] : %s" % (ms.date, ms.chat.title, ms.chat.first_name, ms.text)
    #     else:
    #         print "[%s : %s : %s] : %s" % (ms.date, ms.chat.title, ms.from_user.first_name, ms.text)

    # store_updates = []
    return updates


