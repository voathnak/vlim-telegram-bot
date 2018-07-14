import telegram
import logging

from vlim_telegram_send import VLTelegram

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


bot = telegram.Bot(token='322557664:AAGFsLMC9Fp78oFfB28sF99v-ZHLHfyUdIc')
print bot.getMe()
updates = bot.getUpdates()
print([u.message.text for u in updates])
bot.sendMessage(chat_id=293534239, text="I'm sorry Dave I'm afraid I can't do that.")
print([str(update.message.chat_id) + " : " + str(update.message.text) for update in updates])

VLTelegram.send("Hello Sir")