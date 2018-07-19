import logging

import telegram
from telegram.error import NetworkError

logger = logging.getLogger("VLIM Bot")

class VLIMTelegram:

    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.bot = telegram.Bot(token='322557664:AAGFsLMC9Fp78oFfB28sF99v-ZHLHfyUdIc')

    def send(self, chat_id, message):
        logger.info("<<<<< Send to : %s : %s" % (chat_id, message))
        self.bot.sendMessage(chat_id=chat_id, text=message)

    def getUpdates(self, offset=None, limit=100, timeout=0, read_latency=2., allowed_updates=None):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        self.bot = telegram.Bot(token='322557664:AAGFsLMC9Fp78oFfB28sF99v-ZHLHfyUdIc')
        # self.bot = telegram.Bot(token='674421101:AAHG9KOKxzJQM_46Ya_B665295yEQmVaAdI')  #vlim_test_bot

        contacts = []
        contact = {}
        contacts.append(contact.update({
            'name': 'Tino',
            'id': '293534239'
        }))

        # print bot.getMe()
        # store_updates = []

        updates = []

        try:
            updates = self.bot.getUpdates(offset=offset, limit=limit, timeout=timeout, read_latency=read_latency,
                                          allowed_updates=allowed_updates)
        except NetworkError:
            logger.error("except NetworkError")

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
