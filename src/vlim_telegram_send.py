import telegram
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = telegram.Bot(token='322557664:AAGFsLMC9Fp78oFfB28sF99v-ZHLHfyUdIc')

class VLTelegram():
    def send(self, message):
        bot.sendMessage(chat_id='293534239', text=message)

